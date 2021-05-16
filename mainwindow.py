from PySide2 import QtCore
from PySide2.QtWidgets import QLineEdit, QMainWindow, QFileDialog ,QMessageBox, QInputDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow
import numpy as np
from PIL import Image
import algorithm

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.encrypt_open.clicked.connect(self.load_image)

        self.ui.encryption_progress.setVisible(False)
        self.ui.encrypt_save.setEnabled(False)
        
    def get_array(self,location):
        image = Image.open(location)
        print('Format: ' + image.format)
        print('Size: ' + str(image.size))
        print('Mode: ' + image.mode)

        data = np.asarray(image)
        print(data.shape)
        return image, data

    def encrypt_image(self,location,key):
        self.ui.encryption_progress.setVisible(True)
        self.ui.encryption_progress.setValue(0)
        image, data = self.get_array(location)

        """
        Offset de imagen basado en el tamaño del producto
        de las dos dimensiones y el elemento "n" de la serie 
        fibonacci
        """
        offset = algorithm.fibbonaci(len(key))
        print(f"Offset = {offset}")
        """

        """
        n_w = len(data) + offset               #New width 
        n_h = len(data[0]) + offset            #New height

        rows = []
        columns = []

        counter = 0
        for dimension in data:              #Loop through x axix
            for pixel in dimension:         #Loop through y axis
                colors = []
                for color in pixel:             #Loop through channels
                    #New pixel 
                    c = algorithm.code_8_bit(color,key,counter) 
                    colors.append(c)

                counter += 1
                if counter % offset == 0:   #Ignored pixel
                    ignored_pixel = []
                    for x in colors:
                        ignored_pixel.append( x * len(columns) % 255)
                    columns.append(ignored_pixel)
                    if len(columns) == n_h:
                        rows.append(columns)
                        columns = []
                        value = int(len(rows) / n_w * 100) 
                        self.ui.encryption_progress.setValue(value)
                        
                columns.append(colors)
                if len(columns) == n_h:
                    rows.append(columns)
                    columns = []
                    value = int(len(rows) / n_w * 100)
                    self.ui.encryption_progress.setValue(value)

        print("Encrypted!")
        self.ui.encrypt_save.setEnabled(True)

        decoded_image = np.array(rows)
        img = Image.fromarray(decoded_image, image.mode)

        filename = 'temp/decoded.png'
        img.save(filename)

        w = self.ui.encrypt_result.width()
        h = self.ui.encrypt_result.height()

        image = QPixmap(filename)

        self.ui.encrypt_result.setPixmap(image.scaled(w,h,QtCore.Qt.KeepAspectRatio))
        self.ui.encrypt_result.setMask(image.mask())
 
    @Slot()
    def load_image(self):
        location = QFileDialog.getOpenFileName(
            self,
            'Abrir archivo',
            '.',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.tif)'
        )[0]

        if location != '':
            w = self.ui.encrypt_original.width()
            h = self.ui.encrypt_original.height()

            image  = QPixmap(location)
            self.ui.encrypt_original.setPixmap(image.scaled(w,h,QtCore.Qt.KeepAspectRatio))
            self.ui.encrypt_original.setMask(image.mask())
            
            key = ''
            while key == '':
                key = QInputDialog.getText(
                    self,
                    'Encriptar imagen',
                    'Inserte su clave para encriptar',
                    QLineEdit.Password
                )[0]

            self.encrypt_image(location,key)

        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo " + location
            )