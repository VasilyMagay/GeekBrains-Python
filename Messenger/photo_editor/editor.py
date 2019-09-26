import sys
import shutil
import os
from PyQt5.QtWidgets import (QMainWindow, QLabel,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.temp_file = ''
        self.init_ui()

    def init_ui(self):
        self.lbl = QLabel(self)

        open_file = QAction(QIcon('open.svg'), 'Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open file')
        open_file.triggered.connect(self.show_open_dialog)

        make_bw = QAction(QIcon(), 'Black and White', self)
        make_bw.setStatusTip('Convert to BW')
        make_bw.triggered.connect(self.convert_to_bw)

        make_gray = QAction(QIcon(), 'Gray', self)
        make_gray.setStatusTip('Convert to gray')
        make_gray.triggered.connect(self.convert_to_gray)

        make_negative = QAction(QIcon(), 'Negative', self)
        make_negative.setStatusTip('Convert to negative')
        make_negative.triggered.connect(self.convert_to_negative)

        make_sepia = QAction(QIcon(), 'Sepia', self)
        make_sepia.setStatusTip('Convert to sepia')
        make_sepia.triggered.connect(self.convert_to_sepia)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(open_file)

        convert_menu = menu_bar.addMenu('Covert to...')
        convert_menu.addAction(make_bw)
        convert_menu.addAction(make_gray)
        convert_menu.addAction(make_negative)
        convert_menu.addAction(make_sepia)

        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle('Photo Editor')
        self.show()

    def closeEvent(self, event):
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        super().closeEvent(event)

    def show_open_dialog(self):
        self.temp_file = ''
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Картики (*.jpg *.png *svg);')[0]
        if filename:
            self.temp_file = 'temp_photo' + filename[-4:]
            shutil.copyfile(filename, self.temp_file)
            self.set_photo()
            print(self.temp_file)

    def set_photo(self):
        if self.temp_file:
            pixmap = QPixmap(self.temp_file).scaledToHeight(400)
            self.lbl.resize(400, 400)
            self.lbl.setPixmap(pixmap)
            # print(filename)

    def convert_photo(self, mode):

        image = Image.open(self.temp_file)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()

        Editor.make_effect(mode, width, height, pix, draw)

        img_tmp = ImageQt(image.convert('RGBA'))

        img_tmp.save(self.temp_file)
        self.set_photo()

    @staticmethod
    def make_effect(mode, width, height, pix, draw):
        if mode == 'bw':
            factor = 50
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    s = a + b + c
                    if s > (((255 + factor) // 2) * 3):
                        a, b, c = 255, 255, 255
                    else:
                        a, b, c = 0, 0, 0
                    draw.point((i, j), (a, b, c))
        elif mode == 'gray':
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    s = (a + b + c) // 3
                    draw.point((i, j), (s, s, s))
        elif mode == 'negative':
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    draw.point((i, j), (255 - a, 255 - b, 255 - c))
        elif mode == 'sepia':
            depth = 30
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    s = (a + b + c)
                    a = s + depth * 2
                    b = s + depth
                    c = s
                    a = 255 if a > 255 else a
                    b = 255 if b > 255 else b
                    c = 255 if c > 255 else c
                    draw.point((i, j), (a, b, c))

    def convert_to_bw(self):
        self.convert_photo('bw')

    def convert_to_gray(self):
        self.convert_photo('gray')

    def convert_to_negative(self):
        self.convert_photo('negative')

    def convert_to_sepia(self):
        self.convert_photo('sepia')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())
