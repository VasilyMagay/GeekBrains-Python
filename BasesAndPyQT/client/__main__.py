import yaml
import logging

from argparse import ArgumentParser
from app import Client


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    handlers=[
        logging.FileHandler("app.main.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}
parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

my_client = Client(
    default_config.get('host'),
    default_config.get('port'),
    default_config.get('buffersize')
)

my_client.connect()

try:
    my_client.listen()

    while True:
        action = input('Enter action: ')
        data = input('Enter data: ')
        my_client.send(action, data)

except KeyboardInterrupt:
    my_client.stop()
    logging.info('Client shutdown')

