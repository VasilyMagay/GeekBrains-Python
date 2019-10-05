import sys
import shutil
import os
from PyQt5.QtWidgets import (QMainWindow, QLabel, qApp, QStatusBar, QInputDialog,
                             QAction, QFileDialog, QApplication, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from sqlalchemy import Column, Integer, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DBImage(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    Data = Column(BLOB)


class Editor(QMainWindow):

    def __init__(self):
        super().__init__()

        self.temp_file = ''
        self.pic_width = 0
        self.pic_height = 0
        self.session = None

        self.init_ui()
        self.init_base()

    def init_ui(self):
        # central_widget = QWidget(self)
        # self.setCentralWidget(central_widget)
        #
        # top_layout = QVBoxLayout(self)
        # central_widget.setLayout(top_layout)

        self.lbl = QLabel(self)
        # self.lbl_size = QLabel(self)

        # top_layout.addWidget(self.lbl_size)
        # top_layout.addWidget(self.lbl)

        open_file = QAction(QIcon('open.svg'), 'Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open file')
        open_file.triggered.connect(self.show_open_dialog)

        save_file = QAction(QIcon(), 'Save', self)
        save_file.setShortcut('Ctrl+S')
        save_file.setStatusTip('Save file to database')
        save_file.triggered.connect(self.save_to_db)

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

        exit_action = QAction(QIcon(), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        change_crop = QAction(QIcon(), 'Crop', self)
        change_crop.setStatusTip('Crop photo')
        change_crop.triggered.connect(self.crop_photo)

        change_resize = QAction(QIcon(), 'Resize', self)
        change_resize.setStatusTip('Resize photo')
        change_resize.triggered.connect(self.resize_photo)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(open_file)
        file_menu.addAction(save_file)
        file_menu.addAction(exit_action)

        convert_menu = menu_bar.addMenu('Convert to...')
        convert_menu.addAction(make_bw)
        convert_menu.addAction(make_gray)
        convert_menu.addAction(make_negative)
        convert_menu.addAction(make_sepia)

        change_menu = menu_bar.addMenu('Change size...')
        change_menu.addAction(change_crop)
        change_menu.addAction(change_resize)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.setGeometry(50, 50, 300, 0)
        self.setWindowTitle('Photo Editor')
        self.show()

    def closeEvent(self, event):
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        super().closeEvent(event)

    def show_open_dialog(self):
        self.temp_file = ''
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Pictures (*.jpg *.png *svg);')[0]
        if filename:
            self.temp_file = 'temp_photo' + filename[-4:]
            shutil.copyfile(filename, self.temp_file)
            self.set_photo()

    def set_photo(self):
        if self.temp_file:
            pixmap = QPixmap(self.temp_file)
            self.pic_width = pixmap.width()
            self.pic_height = pixmap.height()
            # pixmap = QPixmap(self.temp_file).scaledToHeight(400)
            self.lbl.resize(self.pic_width, self.pic_height)
            self.lbl.setPixmap(pixmap)

            # text = f'Width {self.pic_width}px, Height {self.pic_height}px'
            # self.lbl_size.setText(text)
            self.setGeometry(50, 50, max(300, self.pic_width), max(200, self.pic_height))

    def convert_photo(self, mode):

        if self.temp_file:
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

    def crop_photo(self):
        if self.pic_width:
            dialog_text = f'Current width {self.pic_width}px, height {self.pic_height}px\n'
            dialog_text += 'Enter crop parameters (left, top, right, bottom):'
            text, ok = QInputDialog.getText(self, 'Input Dialog', dialog_text)
            if ok:
                params = str(text).split(',')
                image = Image.open(self.temp_file)
                image = image.crop((int(params[0]), int(params[1]), int(params[2]), int(params[3])))

                img_tmp = ImageQt(image.convert('RGBA'))
                img_tmp.save(self.temp_file)
                self.set_photo()

    def resize_photo(self):
        if self.pic_width:
            dialog_text = f'Current width {self.pic_width}px, height {self.pic_height}px\n'
            dialog_text += 'Enter resize parameters (width, height):'
            text, ok = QInputDialog.getText(self, 'Input Dialog', dialog_text)
            if ok:
                params = str(text).split(',')
                image = Image.open(self.temp_file)
                image = image.resize((int(params[0]), int(params[1])), Image.NEAREST)

                img_tmp = ImageQt(image.convert('RGBA'))
                img_tmp.save(self.temp_file)
                self.set_photo()

    def init_base(self):

        engine = create_engine('sqlite:///images.db')
        engine.echo = False

        self.session = sessionmaker()
        self.session.configure(bind=engine)
        Base.metadata.create_all(engine)

    def save_to_db(self):
        if self.temp_file:
            with open(self.temp_file, "rb") as file:
                our_pict = file.read()

                s = self.session()
                images = DBImage(Data=our_pict)
                s.add(images)
                s.commit()

                QMessageBox.about(self, 'Info', 'Photo was saved to database')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())
