import yaml
import select
import logging
import logging.handlers as handlers

from socket import socket
from argparse import ArgumentParser

from handlers import handle_default_request

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
        except :
            pass

        if not connections:
            continue

        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for r_client in rlist:
            b_request = r_client.recv(default_config.get('buffersize'))
            requests.append(b_request)

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)
            for w_client in wlist:
                w_client.send(b_response)

except KeyboardInterrupt:
    logging.info('Server shutdown')
