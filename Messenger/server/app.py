import select
import threading
import logging
import asyncio
from socket import socket


class Server:
    def __init__(self, host, port, buffersize, handler):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._handler = handler
        self._connections = list()
        self._requests = list()
        self._sock = None

    def __enter__(self):
        if not self._sock:
            self._sock = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Server shutdown'
        if self._sock:
            self._sock.close()
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = f'Server stopped with error ({exc_type}, {exc_val})'
            logging.error(message, exc_info=exc_val)
        else:
            logging.info(message)
        return True

    def start(self, backlog=5):
        if not self._sock:
            self._sock = socket()
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

    def read(self, client_sock):
        try:
            b_request = client_sock.recv(self._buffersize)
        except ConnectionResetError as err:
            self._connections.remove(client_sock)
            logging.info('Client connection was lost', exc_info=err)
        except Exception as err:
            logging.critical('Read exception raised', exc_info=err)
        else:
            if b_request:
                self._requests.append(b_request)

    def write(self, client_sock, response):
        try:
            client_sock.send(response)
        except Exception as err:
            # self._connections.remove(client_sock)
            logging.critical('Write exception raised', exc_info=err)


class AsyncServer:
    def __init__(self, host, port, buffersize, handler):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._handler = handler
        self._connections = list()
        self._requests = list()

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Server shutdown'
        if self._sock:
            self._sock.close()
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = f'Server stopped with error ({exc_type}, {exc_val})'
            logging.error(message, exc_info=exc_val)
        else:
            logging.info(message)
        return True

    async def main(self):

        while True:

            try:
                client, address = self._sock.accept()
                if client:
                    self._connections.append(client)
                    logging.info(
                        f'Client was connected with {address[0]}:{address[1]} | Connections: {len(self._connections)}')
            except Exception:
                pass
            else:
                client.setblocking(0)  # снимаем блокировку и у клиента тоже

            if not self._connections:
                continue

            rlist, wlist, xlist = select.select(self._connections, self._connections, self._connections, 0)

            await self.read(rlist)
            await self.write(wlist)

    def start(self, backlog=5):

        self._sock = socket()
        self._sock.bind((self._host, self._port,))
        self._sock.settimeout(0)  # sock.setblocking(False)
        self._sock.listen(backlog)
        logging.info(f'Server was started with {self._host}:{self._port}')

        ioloop = asyncio.get_event_loop()
        ioloop.run_until_complete(self.main())
        ioloop.close()

    async def read(self, client_socks):
        for client_sock in client_socks:
            try:
                b_request = client_sock.recv(self._buffersize)
                if b_request:
                    self._requests.append(b_request)
            except Exception:
                pass
            print(f'read from to {client_sock}')
            await asyncio.sleep(1)

    async def write(self, client_socks):
        if self._requests:
            b_request = self._requests.pop()
            b_response = self._handler(b_request)
            for client_sock in client_socks:
                try:
                    client_sock.send(b_response)
                except Exception:
                    pass
                print(f'write to {client_sock}')
                await asyncio.sleep(1)
