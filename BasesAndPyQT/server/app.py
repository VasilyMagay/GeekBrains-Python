import select
import threading
import logging
from socket import socket


class ServerVerifier(type):
    def __new__(cls, clsname, bases, clsdict):
        return type.__new__(cls, clsname, bases, clsdict)

    def __init__(self, clsname, bases, clsdict):
        # for key, value in clsdict.items():
        #     print(f'{key}={value}')
        type.__init__(self, clsname, bases, clsdict)


class Server(metaclass=ServerVerifier):
    def __init__(self, host, port, buffersize, handler):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._handler = handler
        self._connections = list()
        self._requests = list()
        self._sock = socket()

    def start(self, backlog=5):
        self._sock.bind((self._host, self._port,))
        self._sock.settimeout(0)  # sock.setblocking(False)
        self._sock.listen(backlog)

        logging.info(f'Server was started with {self._host}:{self._port}')

    def wait_client(self):
        try:
            client, address = self._sock.accept()
        except Exception:
            pass
        else:
            self._connections.append(client)
            logging.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {len(self._connections)}')

    def processing(self):
        try:
            while True:

                self.wait_client()

                if not self._connections:  # Без данной проверки выдает ошибку при первом старте
                    continue

                rlist, wlist, xlist = select.select(
                    self._connections, self._connections, self._connections, 0
                )

                for r_client in rlist:
                    r_thread = threading.Thread(
                        target=self.read, args=(r_client,)
                    )
                    r_thread.start()

                if self._requests:
                    b_request = self._requests.pop()
                    b_response = self._handler(b_request)
                    for w_client in wlist:
                        w_thread = threading.Thread(
                            target=self.write, args=(w_client, b_response)
                        )
                        w_thread.start()

        except KeyboardInterrupt:
            self.stop()

    def read(self, client_sock):
        try:
            b_request = client_sock.recv(self._buffersize)
        except Exception:
            self._connections.remove(client_sock)
        else:
            if b_request:
                self._requests.append(b_request)

    def write(self, client_sock, response):
        try:
            client_sock.send(response)
        except Exception:
            self._connections.remove(client_sock)

    def stop(self):
        logging.info('Server shutdown')
        self._sock.close()
