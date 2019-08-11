import zlib
import yaml
import json
import logging
import hashlib
import threading

from socket import socket
from datetime import datetime
from argparse import ArgumentParser


def read(sock, buffersize):
    while True:
        comporessed_response = sock.recv(buffersize)
        b_response = zlib.decompress(comporessed_response)
        logging.info(b_response.decode())


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

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    handlers=[
        logging.FileHandler("app.main.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'))
)

logging.info('Client was started')

try:
    read_thread = threading.Thread(
        target=read, args=(sock, default_config.get('buffersize'),)
    )
    read_thread.start()

    while True:
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = {
            'action': action,
            'time': datetime.now().timestamp(),
            'data': data,
            'token': hash_obj.hexdigest()
        }

        s_request = json.dumps(request)
        b_request = zlib.compress(s_request.encode())
        sock.send(b_request)
        logging.info(f'Client send data: {data}')

except KeyboardInterrupt:
    sock.close()
    logging.info('Client shutdown')
