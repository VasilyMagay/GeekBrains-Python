import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QApplication, QVBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QAction, QFileDialog,
    QMainWindow
)
from app import Client
from utils import read_config
from PyQt5.QtGui import QPixmap, QIcon


class Registration(QWidget):

    def __init__(self, host, port, buffersize):
        super().__init__()

        self.init_ui()

        self._host = host
        self._port = port
        self._buffersize = buffersize

    def init_ui(self):

        window = QMainWindow(self)

        # Меню

        open_file = QAction(QIcon('open.svg'), 'Change', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Изменить фото')
        open_file.triggered.connect(self.show_open_dialog)

        menu_bar = window.menuBar()
        photo_menu = menu_bar.addMenu('Photo')
        photo_menu.addAction(open_file)

        # Photo

        self.label_photo = QLabel(self)
        self.set_photo()

        # Name

        label_name = QLabel()
        label_name.setText('Name:')
        label_name.setMaximumHeight(24)

        self.text_name = QLineEdit()
        self.text_name.setFixedHeight(24)
        self.text_name.setFixedWidth(200)

        name_layout = QHBoxLayout()
        name_layout.addWidget(label_name)
        name_layout.addWidget(self.text_name)

        # Password

        label_password = QLabel()
        label_password.setText('Password:')
        label_password.setMaximumHeight(24)

        self.text_password = QLineEdit()
        self.text_password.setFixedHeight(24)
        self.text_password.setFixedWidth(200)
        self.text_password.setEchoMode(QLineEdit.Password)

        password_layout = QHBoxLayout()
        password_layout.addWidget(label_password)
        password_layout.addWidget(self.text_password)

        # Кнопка

        register_button = QPushButton("Register", self)
        register_button.clicked.connect(self.click_register_button)

        # Вывод

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(menu_bar)
        main_layout.addWidget(self.label_photo)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(password_layout)
        main_layout.addWidget(register_button)

        self.setLayout(main_layout)
        self.move(300, 200)
        self.setWindowTitle('Registration Form')
        self.show()

    def click_register_button(self):
        self.register(self.text_name.text(), self.text_password.text())

    def register(self, login, password):
        with Client(self._host, self._port, self._buffersize) as client:
            result = client.send('registrate', data={'login': login, 'password': password})
            # print(f'result={result}')
            response = None
            for i in range(100):
                response = client.read_response(result.get('token'))
                # print(f'{i}: {data}')
                if response:
                    QMessageBox.information(self, "Info", f'{response.get("data")}')
                    break
                # sleep(3)
            if not response:
                QMessageBox.about(self, 'Info', 'Timeout error')

    def set_photo(self):
        if os.path.exists('profile/logo.jpg'):
            filename = 'profile/logo.jpg'
        else:
            filename = 'no-image-icon.png'
        pixmap = QPixmap(filename)
        self.label_photo.setPixmap(pixmap.scaledToWidth(200))

    def show_open_dialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Картики (*.jpg);')[0]
        if filename:
            shutil.copyfile(filename, 'profile/logo.jpg')
            self.set_photo()


if __name__ == '__main__':
    config = read_config()

    app = QApplication(sys.argv)
    form = Registration(config.get('host'), config.get('port'), config.get('buffersize'))
    sys.exit(app.exec_())
