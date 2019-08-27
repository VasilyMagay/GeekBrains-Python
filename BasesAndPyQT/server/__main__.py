import yaml
import select
import logging
import logging.handlers as handlers
import threading

from socket import socket
from argparse import ArgumentParser

from handlers import handle_default_request


def read(sock, connections, requests, buffersize):
    try:
        b_request = sock.recv(buffersize)
    except Exception:
        connections.remove(sock)
    else:
        if b_request:
            requests.append(b_request)


def write(sock, connection, response):
    try:
        sock.send(response)
    except Exception:
        connection.remove(sock)


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

host, port = (default_config.get('host'), default_config.get('port'))

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    handlers=[
        handlers.TimedRotatingFileHandler("app.main.log", when='D', interval=1, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

connections = []
requests = []

try:

    sock = socket()
    sock.bind((host, port,))
    sock.settimeout(0)  # sock.setblocking(False)
    sock.listen(5)

    logging.info(f'Server was started with {host}:{port}')

    while True:

        try:
            client, address = sock.accept()
            connections.append(client)
            logging.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {len(connections)}')
        except Exception:
            pass

        if not connections:
            continue

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for r_client in rlist:
            r_thread = threading.Thread(
                target=read, args=(r_client, connections, requests, default_config.get('buffersize'))
            )
            r_thread.start()

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)
            for w_client in wlist:
                w_thread = threading.Thread(
                    target=write, args=(w_client, connections, b_response)
                )
                w_thread.start()

except KeyboardInterrupt:
    logging.info('Server shutdown')
