import yaml
import json
from datetime import datetime
from socket import socket
from argparse import ArgumentParser


def presence_message(account, status='', message_type=None):
    res = {
        "action": "presence",
        "time": str(datetime.utcnow()),
        "user": {
            "account_name": account,
            "status": status
        }
    }

    if message_type is not None:
        res['type'] = message_type

    return res


MY_ACCOUNT = 'BroTheRS'

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
    sock.connect(
        (default_config.get('host'), default_config.get('port'))
    )

    print('Client was started')

except ConnectionRefusedError:
    print('Server not started. Try later.')
    exit()

json_data = presence_message(MY_ACCOUNT, "'I'm online")
json_string = json.dumps(json_data)
sock.send(json_string.encode())

print(f'Client send action: {json_data["action"]}')

b_response = sock.recv(default_config.get('buffersize'))
json_string = b_response.decode()
json_data = json.loads(json_string)
print(f'Response code: {json_data["response"]}, time: {json_data["time"]}')
if json_data["response"] <= 200:
    print(f'Message from server: {json_data["alert"]}')
