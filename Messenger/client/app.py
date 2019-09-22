import logging
import threading
import hashlib
import zlib
import json
import sys
from socket import socket
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
    QDesktopWidget
)
from array import array
from itertools import islice

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Client:
    def __init__(self, host, port, buffersize):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._sock = socket()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown'
        if self._sock:
            self._sock.close()
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = 'Client stopped with error'
            logging.error(message, exc_info=exc_val)
        else:
            logging.info(message)
        return True

    def connect(self):
        try:
            self._sock.connect((self._host, self._port))
        except Exception as err:
            logging.critical(f'Client connect error ({self._host}:{self._port})', exc_info=err)
        else:
            logging.info(f'Client was started ({self._host}:{self._port})')

    def listen(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

    def read(self):
        while True:
            try:
                compressed_response = self._sock.recv(self._buffersize)
            except Exception:
                pass
            else:
                encrypted_response = zlib.decompress(compressed_response)

                nonce, encrypted_response = get_chunk(encrypted_response, 16)
                key, encrypted_response = get_chunk(encrypted_response, 16)
                tag, encrypted_response = get_chunk(encrypted_response, 16)

                cipher = AES.new(key, AES.MODE_EAX, nonce)

                raw_response = cipher.decrypt_and_verify(encrypted_response, tag)
                string_response = raw_response.decode()
                logging.info(string_response)

                response = json.loads(raw_response)
                data = response.get('data')
                self.message_list.append(data)

    def send(self, action, data):

        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )
        token = hash_obj.hexdigest()

        request = make_request(action, data, token)
        byte_request = json.dumps(request).encode()

        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        encrypt_request, tag = cipher.encrypt_and_digest(byte_request)

        # cipher.nonce - идентификатор шифра
        compress_request = zlib.compress(
            b'%(nonce)s%(key)s%(tag)s%(data)s' % {
                b'nonce': cipher.nonce, b'key': key, b'tag': tag, b'data': encrypt_request
            }
        )

        self.message_text.clear()
        self._sock.send(compress_request)

        logging.info(f'Client send data: {data}')

    def init_ui(self):

        app = QApplication(sys.argv)

        window = QMainWindow()
        # Установка заголовка и размеров главного окна
        window.setGeometry(400, 600, 400, 600)
        window.setWindowTitle('Messenger')

        self.send_button = QPushButton("Send", window)
        self.send_button.clicked.connect(self.click_send_button)
        self.send_button.setMaximumHeight(64)

        self.message_text = QTextEdit()
        self.message_text.setMaximumHeight(64)

        self.message_list_label = QLabel("Messages:")

        self.message_list = QTextEdit()
        self.message_list.setReadOnly(True)

        main_layout = QVBoxLayout()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.message_list_label)
        top_layout.addWidget(self.message_list)

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(self.message_text)
        footer_layout.addWidget(self.send_button)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(footer_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        window.setCentralWidget(central_widget)

        dsk_widget = QDesktopWidget()
        geometry = dsk_widget.availableGeometry()
        center_position = geometry.center()
        frame_geometry = window.frameGeometry()
        frame_geometry.moveCenter(center_position)
        window.move(frame_geometry.topLeft())

        window.show()
        sys.exit(app.exec_())

    def click_send_button(self):
        self.send('echo', self.message_text.toPlainText())

    def run(self):
        self.listen()
        self.init_ui()


def get_chunk(text, size):
    text_iter = (char for char in text)
    chunk = array('B', islice(text_iter, size)).tobytes()
    text_residue = array('B', text_iter).tobytes()
    return chunk, text_residue


def make_request(action, data, token):
    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'token': token
    }
    if isinstance(data, dict):
        request.update(data)
    else:
        request['data'] = data
    return request
