from app import Client
from utils import read_config

if __name__ == '__main__':
    config = read_config()

    with Client(
            config.get('host'), config.get('port'), config.get('buffersize'),
            config.get('username'), config.get('password')
    ) as my_client:
        my_client.run()
