from PySide2 import QtCore
from PySide2.QtWidgets import QLineEdit, QMainWindow, QFileDialog ,QMessageBox, QInputDialog
from PySide2.QtCore import QLine, Slot
from PySide2.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow
import numpy as np
from PIL import Image
import random

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.encrypt_open.clicked.connect(self.load_image)
        
    def get_array(self,location):
        image = Image.open(location)
        print('Format: ' + image.format)
        print('Size: ' + str(image.size))
        print('Mode: ' + image.mode)

        data = np.asarray(image)
        print(data.shape)
        return image, data

    def fibbonaci(self,number):
        a, b = 0, 1
        for _ in range(number):
            a, b = b, a+b
        return b

    def reverse_fibonacci(self,number):
        a, b = 0, 1
        counter = 0
        while number >= b:
            if number == b:
                return counter
            a, b = b, a+b
            counter += 1
        return 0 

    def encrypt_image(self,location,key):
        image, data = self.get_array(location)

        """
        Offset de imagen basado en el tamaño del producto
        de las dos dimensiones y el elemento "n" de la serie 
        fibonacci
        """
        offset = self.fibbonaci(len(key))
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
                    c = self.code_8_bit(color,key,counter) #New pixel
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
                        
                columns.append(colors)
                if len(columns) == n_h:
                    rows.append(columns)
                    columns = []
        
        # print(counter)
        
        # print(len(rows))
        # print(len(rows[0]))
        # print(len(rows[0][0]))
        # print(len(rows[len(rows)-1]))

        print("Encrypted!")

        decoded_image = np.array(rows)
        img = Image.fromarray(decoded_image, image.mode)
        img.save('temp/decoded.png')
        img.show()


    def code_8_bit(self,value,key,position):
        """XOR CYPHER"""
        position = position % len(key) 
        key = ord(key[position])            #Get ASCII code
        value = '{0:08b}'.format(value)
        key = '{0:08b}'.format(key)

        result = []
        for i in range(len(value)):
            if value[i] == key[i]:
                result += "1"
            else:
                result += "0"
        result = "".join( str(bit) for bit in result )
        return int(result,2) 



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