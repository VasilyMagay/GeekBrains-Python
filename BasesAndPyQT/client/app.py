import logging
import threading
import hashlib
import zlib
import json
from socket import socket
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QTextEdit,
    QPlainTextEdit, QWidget, QVBoxLayout
)
from PyQt5 import QtCore


class Client(QMainWindow):
    def __init__(self, host, port, buffersize):
        super().__init__()
        self.init_ui()

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
                s_response = b_response.decode()
                logging.info(s_response)
                self.message_list.setPlainText(s_response)

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

    def init_ui(self):

        self.send_button = QPushButton("Send Message", self)
        self.send_button.clicked.connect(self.click_send_button)

        self.message_label = QLabel("Message:")

        self.message_text = QTextEdit()
        self.message_text.setGeometry(QtCore.QRect(10, 10, 370, 50))

        self.message_list_label = QLabel("Protocol:")

        self.message_list = QPlainTextEdit()
        self.message_list.setGeometry(QtCore.QRect(10, 10, 370, 200))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.message_list_label)
        main_layout.addWidget(self.message_list)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.message_text)
        main_layout.addWidget(self.send_button)
        # main_layout = QGridLayout()
        # main_layout.addWidget(self.message_label, 0, 0, QtCore.Qt.AlignTop)
        # main_layout.addWidget(self.message_text, 0, 1)
        # main_layout.addWidget(self.send_button, 1, 0)


        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        # Установка заголовка и размеров главного окна
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Messenger')

    def click_send_button(self):
        self.send('echo', self.message_text.toPlainText())
