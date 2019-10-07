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
    QDesktopWidget, QMessageBox
)
from array import array
from itertools import islice

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Client(QMainWindow):
    def __init__(self, host, port, buffersize, username='', password=''):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._sock = socket()
        self._session_token = None
        self._username = username
        self._password = password
        self._connected = False

        self.app = QApplication(sys.argv)
        super().__init__()
        self.init_ui()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown'
        if self._sock:
            self._sock.close()
        if exc_type:
            # print(f'exc_type={exc_type}')
            if exc_type not in (SystemExit, KeyboardInterrupt):
                message = 'Client stopped with error'
                logging.error(message, exc_info=exc_val)
        else:
            logging.info(message)
        return True

    def closeEvent(self, event):
        self.logout()
        message = 'Client shutdown'
        if self._sock:
            self._sock.close()
        logging.info(message)
        super().closeEvent(event)

    def connect(self):
        try:
            self._sock.connect((self._host, self._port))
            self._connected = True
        except Exception as err:
            logging.critical(f'Client connect error ({self._host}:{self._port})', exc_info=err)
        else:
            logging.info(f'Client was started ({self._host}:{self._port})')

    def listen(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()

    def read(self):
        while True:
            response = self.read_response()
            if response:
                action = response.get('action')
                if action == 'echo':
                    message = f'{response.get("username")}: {response.get("data")}'
                    if response.get("username") == self._username:
                        message = f'<b>{message}</b>';
                    else:
                        message = f'<i>{message}</i>';
                    self.message_list.append(message)
                elif action == 'logout' and response.get('token') == self._session_token:
                    self._session_token = ''
                    self.send_button.hide()
                    self.message_text.hide()
                    self.login_button.show()
                    self.logout_button.hide()

    def read_response(self, return_token=''):
        response = None
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
            if return_token and response.get('token') != return_token:
                response = None

        return response

    def send(self, action, data):

        if self._session_token:
            token = self._session_token
        else:
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

        # self.message_text.clear()
        self._sock.send(compress_request)

        logging.info(f'Client send data: {data}')

        return {'token': token}

    def init_ui(self):

        # Установка заголовка и размеров главного окна
        self.setGeometry(400, 600, 400, 600)
        self.setWindowTitle('Messenger')

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.click_login_button)
        self.login_button.setMaximumHeight(64)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.click_logout_button)
        self.logout_button.setMaximumHeight(64)
        self.logout_button.hide()

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.click_send_button)
        self.send_button.setMaximumHeight(64)
        self.send_button.hide()

        self.message_text = QTextEdit()
        self.message_text.setMaximumHeight(64)
        self.message_text.hide()

        self.message_list_label = QLabel("Messages:")

        self.message_list = QTextEdit()
        self.message_list.setReadOnly(True)

        user_label = QLabel(f'User: {self._username}')

        main_layout = QVBoxLayout()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.message_list_label)
        top_layout.addWidget(self.message_list)

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(self.message_text)
        footer_layout.addWidget(self.send_button)

        main_layout.addWidget(user_label)
        main_layout.addWidget(self.login_button)
        main_layout.addWidget(self.logout_button)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(footer_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        dsk_widget = QDesktopWidget()
        geometry = dsk_widget.availableGeometry()
        center_position = geometry.center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_position)
        self.move(frame_geometry.topLeft())

    def click_send_button(self):
        self.send('echo', self.message_text.toPlainText())
        self.message_text.clear()

    def click_login_button(self):

        if not self._connected:
            self.connect()

        if not self._connected:
            QMessageBox.about(self, 'Info', 'Server not active')
            return

        result = self.send('login', {'login': self._username, 'password': self._password})

        data = None
        for i in range(100):
            response = self.read_response(result.get('token'))
            data = response.get('data')
            # print(f'{i}: {data}')
            if data:
                if 'token' in data:
                    self._session_token = data.get('token')
                    self.send_button.show()
                    self.message_text.show()
                    self.login_button.hide()
                    self.logout_button.show()
                    self.listen()  # начинаем прием сообщений
                else:
                    QMessageBox.information(self, "Info", f'{data}')
                break
            # sleep(3)
        if not data:
            QMessageBox.about(self, 'Info', 'Timeout error')

        # print(f'data={data}')

    def run(self):
        self.show()
        sys.exit(self.app.exec_())

    def logout(self):
        if self._session_token:
            self.send('logout', {})

    def click_logout_button(self):
        self.logout()


def get_chunk(text, size):
    text_iter = (char for char in text)
    chunk = array('B', islice(text_iter, size)).tobytes()
    text_residue = array('B', text_iter).tobytes()
    return chunk, text_residue


def make_request(action, data, token):
    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'token': token,
        'data': data,
    }
    return request
