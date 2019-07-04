import yaml
import json
from datetime import datetime
from socket import socket
from argparse import ArgumentParser

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

try:

    sock = socket()
    sock.bind(
        (default_config.get('host'), default_config.get('port'))
    )
    sock.listen(5)

    print(f'Server was started with {default_config.get("host")}:{default_config.get("port")}')

    while True:

        client, address = sock.accept()
        print(f'Client was connected with {address[0]}:{address[1]}')

        b_request = client.recv(default_config.get('buffersize'))
        json_string = b_request.decode()
        json_data = json.loads(json_string)
        print(f'Client send action: {json_data["action"]}, time: {json_data["time"]}')

        alert = ''
        error = ''
        if json_data["action"] == 'presence':
            response_code = 200
            alert = f'Hi, {json_data["user"]["account_name"]}'
        else:
            response_code = 400
            error = 'неправильный запрос/JSON-объект'

        json_data = {
            "response": response_code,
            "time": str(datetime.utcnow())
        }

        if response_code <= 200 and len(alert) > 0:
            json_data['alert'] = alert
        if response_code >= 400 and len(error) > 0:
            json_data['error'] = error

        json_string = json.dumps(json_data)
        client.send(json_string.encode())
        client.close()

except KeyboardInterrupt:

    print('Server shutdown')
