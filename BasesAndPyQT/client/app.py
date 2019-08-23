import logging
import threading
import hashlib
import zlib
import json
from socket import socket
from datetime import datetime


class ClientVerifier(type):
    def __new__(cls, clsname, bases, clsdict):
        return type.__new__(cls, clsname, bases, clsdict)

    def __init__(self, clsname, bases, clsdict):
        # for key, value in clsdict.items():
        #     print(f'{key}={value}')
        type.__init__(self, clsname, bases, clsdict)


class Client(metaclass=ClientVerifier):
    def __init__(self, host, port, buffersize):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._sock = socket()

    def connect(self):
        try:
            self._sock.connect((self._host, self._port))
        except Exception:
            logging.error(f'Client connect error ({self._host}:{self._port})')
        else:
            logging.info(f'Client was started ({self._host}:{self._port})')

    def listen(self):
        read_thread = threading.Thread(
            target=self.read, args=tuple()
        )
        read_thread.start()

    def read(self):
        while True:
            try:
                compressed_response = self._sock.recv(self._buffersize)
            except Exception:
                pass
            else:
                b_response = zlib.decompress(compressed_response)
                logging.info(b_response.decode())

    def send(self, action, data):
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        request = {
            'action': action,
            'time': datetime.now().timestamp(),
            # 'data': data,
            'token': hash_obj.hexdigest()
        }

        if isinstance(data, dict):
            request.update(data)
        else:
            request['data'] = data

        s_request = json.dumps(request)
        b_request = zlib.compress(s_request.encode())
        self._sock.send(b_request)
        logging.info(f'Client send data: {data}')

    def stop(self):
        self._sock.close()
