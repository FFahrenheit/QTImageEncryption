from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QFileDialog ,QMessageBox
from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow
import numpy as np
from PIL import Image

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.encrypt_open.clicked.connect(self.load_image)
        
    def encrypt_image(self,location):
        image = Image.open(location)
        print('Format: ' + image.format)
        print('Size: ' + str(image.size))
        print('Mode: ' + image.mode)

        data = np.asarray(image)
        print(len(data))
        print(data.shape)

        key = '123'

        rows = []
        for dimension in data:          #Loop through x axix
            columns = []
            for pixel in dimension:     #Loop through y axis
                colors = []
                for color in pixel:     #Loop through channels
                    colors.append(0)
                columns.append(colors)
            rows.append(columns)
        
        print(len(rows))
        print(len(rows[0]))
        print(len(rows[0][0]))

    def code_8_bit(self,key):
        print(key)

    @Slot()
    def load_image(self):
        location = QFileDialog.getOpenFileName(
            self,
            'Abrir archivo',
            '.',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.tif)'
        )[0]

        if location != '':
            QMessageBox.information(
                self,
                "Éxito",
                "Se abrió el archivo " + location
            )
            w = self.ui.encrypt_original.width()
            h = self.ui.encrypt_original.height()

            image  = QPixmap(location)
            self.ui.encrypt_original.setPixmap(image.scaled(w,h,QtCore.Qt.KeepAspectRatio))
            self.ui.encrypt_original.setMask(image.mask())
            self.encrypt_image(location)

        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo " + location
            )