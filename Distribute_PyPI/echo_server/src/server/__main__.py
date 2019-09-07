import yaml
import logging
import logging.handlers as handlers

from argparse import ArgumentParser
from handlers import handle_default_request
from app import Server

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    handlers=[
        handlers.TimedRotatingFileHandler("app.main.log", when='D', interval=1, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

with Server(
        default_config.get('host'),
        default_config.get('port'),
        default_config.get('buffersize'),
        handle_default_request) as my_server:
    my_server.start()
    my_server.processing()
