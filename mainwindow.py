from PySide2 import QtCore
from PySide2.QtWidgets import QLineEdit, QMainWindow, QFileDialog ,QMessageBox, QInputDialog
from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from numpy.core.numeric import full
from ui_mainwindow import Ui_MainWindow
import numpy as np
from PIL import Image
import algorithm

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.encrypt_open.clicked.connect(self.load_encrypt_image)
        self.ui.decrypt_open.clicked.connect(self.load_decrypt_image)

        self.ui.encryption_progress.setVisible(False)
        self.ui.encrypt_save.setEnabled(False)
        self.ui.decryption_progress.setVisible(False)
        self.ui.decrypt_save.setEnabled(False)
        
    def get_array(self,location):
        image = Image.open(location)
        print('Format: ' + image.format)
        print('Size: ' + str(image.size))
        print('Mode: ' + image.mode)

        data = np.uint8(np.array(image))
        print(data.shape)
        print(data)
        return image, data

    def decrypt_image(self,location,key):
        self.ui.decryption_progress.setVisible(True)
        self.ui.decryption_progress.setValue(0)
        image, data = self.get_array(location)

        offset = algorithm.fibbonaci(len(key))
        print(f"Offset = {offset}")

        n_h = len(data[0]) - offset
        print(f"nh = {n_h}")

        print(f"Offset2 = {offset}")

        rows = []
        columns = []

        counter = 0
        aux = 0
        full_counter = 0

        for (index,dimension) in enumerate(data):                   #Loop through x axix
            for pixel in dimension:                                 #Loop through y axis
                colors = []
                for color in pixel:                                 #Loop through channels
                    #New pixel 
                    c = algorithm.code_8_bit(color,key,full_counter)
                    colors.append(c)

                aux += 1
                if full_counter % offset != 0:
                    counter += 1
                    columns.append(colors)
                    if len(columns) == n_h:
                        rows.append(columns)
                        columns = []
                        value = int(index / len(data) * 100)
                        if value != self.ui.decryption_progress.value() != value:
                            self.ui.decryption_progress.setValue(value)
                
                full_counter += 1

        print(len(rows))
        print(len(rows[0]))
        print(len(rows[0][0]))
        print("Desencrypted!")
        print(f"Counter = {counter}, full = {full_counter}")
        self.ui.decrypt_save.setEnabled(True)
        self.ui.decryption_progress.setValue(100)

        count = 0
        for i in range(len(data)*len(data[0])):
            if i % offset == 0:
                count += 1

        print(f"Final Count: {count}")
        count = 0
        errors = 0
        for x in rows:
            if len(x) != n_h:
                errors += 1
            for y in x:
                count += 1
        
        print(f"Final count = {count}, errors = {errors}")

        decoded_image = np.array(rows)
        img = Image.fromarray(np.uint8(decoded_image),image.mode)

        filename = 'temp/decoded.' + str(image.format).lower()
        img.save(filename)

        w = self.ui.decrypt_result.width()
        h = self.ui.decrypt_result.height()

        image = QPixmap(filename)

        self.ui.decrypt_result.setPixmap(image.scaled(w,h,QtCore.Qt.KeepAspectRatio))
        self.ui.decrypt_result.setMask(image.mask())

        self.get_array(filename)



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
        
        n_h = len(data[0]) + offset               #New height
        print(f"nh = {n_h}")

        # offset = algorithm.fibbonaci(offset)
        print(f"Offset2 = {offset}")

        rows = []
        columns = []

        counter = 0
        full_counter = 0
        total_black = 0

        for (index, dimension) in enumerate(data):              #Loop through x axix
            for pixel in dimension:                             #Loop through y axis
                colors = []
                for color in pixel:                             #Loop through channels
                    #New pixel 
                    c = algorithm.code_8_bit(color,key,full_counter) 
                    c = color
                    colors.append(c)
                if  full_counter % offset == 0:   #Ignored pixel
                        
                    full_counter += 1
                    ignored_pixel = []
                    for x in colors:
                        ignored_pixel.append( x * len(columns) % 255)
                        # ignored_pixel.append(0)
                    columns.append(ignored_pixel)
                    if len(columns) == n_h:
                        rows.append(columns)
                        columns = []
                counter += 1
                full_counter += 1

                columns.append(colors)
                if len(columns) == n_h:
                    rows.append(columns)
                    columns = []
                    value = int(index/len(data)*100)
                    if self.ui.encryption_progress.value() != value:
                        self.ui.encryption_progress.setValue(value)

        if len(columns) > 0:
            for _ in range(n_h - len(columns)):
                columns.append([0, 0, 0])
            rows.append(columns)
        
        print("Encrypted!")
        print(f"Count = {counter}, full = {full_counter}")
        self.ui.encrypt_save.setEnabled(True)
        self.ui.encryption_progress.setValue(100)

        decoded_image = np.array(rows)
        img = Image.fromarray(np.uint8(decoded_image),image.mode)

        filename = 'temp/encoded.' + str(image.format).lower()

        img.save(filename)

        count = 0

        for x in rows:
            for y in x:
                count += 1

        print(f"Final count: {count}")

        w = self.ui.encrypt_result.width()
        h = self.ui.encrypt_result.height()

        image = QPixmap(filename)

        self.ui.encrypt_result.setPixmap(image.scaled(w,h,QtCore.Qt.KeepAspectRatio))
        self.ui.encrypt_result.setMask(image.mask())

        self.get_array(filename)

 
    @Slot()
    def load_decrypt_image(self):
        location = QFileDialog.getOpenFileName(
            self,
            'Abrir archivo',
            '.',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.tif)'
        )[0]

        if location != '':
            w = self.ui.decrypt_original.width()
            h = self.ui.decrypt_original.height()

            image  = QPixmap(location)
            self.ui.decrypt_original.setPixmap(image.scaled(w,h,QtCore.Qt.KeepAspectRatio))
            self.ui.decrypt_original.setMask(image.mask())
            
            key = ''
            while key == '':
                key = QInputDialog.getText(
                    self,
                    'Desencriptar imagen',
                    'Inserte su clave para encriptar',
                    QLineEdit.Password
                )[0]

            self.decrypt_image(location,str(key))

        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo " + location
            )

    @Slot()
    def load_encrypt_image(self):
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

            self.encrypt_image(location,str(key))

        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo " + location
            )