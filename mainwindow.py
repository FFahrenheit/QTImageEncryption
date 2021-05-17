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

        self.ui.encrypt_open.clicked.connect(self.load_encrypt_image)
        self.ui.decrypt_open.clicked.connect(self.load_decrypt_image)

        self.ui.decrypt_save.clicked.connect(self.save_decrypt)
        self.ui.encrypt_save.clicked.connect(self.save_encrypt)

        self.ui.encryption_progress.setVisible(False)
        self.ui.encrypt_save.setEnabled(False)
        self.ui.decryption_progress.setVisible(False)
        self.ui.decrypt_save.setEnabled(False)
    
    @Slot()
    def save_encrypt(self):
        location = QFileDialog.getSaveFileName(
            self,
            'Guardar imagen',
            '.',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.tif)'
        )[0]
        location = location + '.' + str(self.enc_original.format).lower()
        print(location)
        self.encrypted_img.save(location)
        QMessageBox.information(
                self,
                "Éxito",
                "Se guardó en el archivo en " + location 
            )

    @Slot()
    def save_decrypt(self):
        location = QFileDialog.getSaveFileName(
            self,
            'Guardar imagen',
            '.',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.tif)'
        )[0]
        location = location + '.' + str(self.dec_original.format).lower()
        print(location)
        self.decrypted_img.save(location)
        QMessageBox.information(
                self,
                "Éxito",
                "Se guardó en el archivo en " + location
            )

    def get_array(self,location):
        image = Image.open(location)
        print('Format: ' + image.format)
        print('Size: ' + str(image.size))
        print('Mode: ' + image.mode)

        data = np.uint8(np.array(image))
        print(data.shape)
        # print(data)
        return image, data

    def decrypt_image(self,location,key):
        self.ui.decryption_progress.setVisible(True)
        self.ui.decryption_progress.setValue(0)
        image, data = self.get_array(location)
        self.dec_original = image

        offset = algorithm.fibbonaci(len(key))

        n_h = len(data[0]) - offset

        rows = []
        columns = []

        counter = 0
        aux = 0
        full_counter = 0

        for (index,dimension) in enumerate(data):                   #Loop through x axix
            for pixel in dimension:                                 #Loop through y axis
                colors = []

                aux += 1
                if full_counter % offset != 0:
                    for color in pixel:                                 #Loop through channels
                    #New pixel 
                        c = algorithm.code_8_bit(color,key,full_counter)
                        colors.append(c)
                    counter += 1
                    columns.append(colors)
                    if len(columns) == n_h:
                        rows.append(columns)
                        columns = []
                        value = int(index / len(data) * 100)
                        if value != self.ui.decryption_progress.value() != value:
                            self.ui.decryption_progress.setValue(value)
                
                full_counter += 1

        print("Desencrypted!")
        self.ui.decrypt_save.setEnabled(True)
        self.ui.decryption_progress.setValue(100)

        decoded_image = np.uint8(np.array(rows))
        img = Image.fromarray(decoded_image,image.mode)

        filename = 'temp/decoded.' + str(image.format).lower()
        img.save(filename)
        self.decrypted_img = img

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
        self.enc_original = image

        """
        Offset de imagen basado en el tamaño del producto
        de las dos dimensiones y el elemento "n" de la serie 
        fibonacci
        """

        offset = algorithm.fibbonaci(len(key))
        
        n_h = len(data[0]) + offset               #New height

        rows = []
        columns = []

        counter = 0
        full_counter = 0

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
        self.ui.encrypt_save.setEnabled(True)
        self.ui.encryption_progress.setValue(100)

        decoded_image = np.uint8(np.array(rows))
        img = Image.fromarray(np.uint8(decoded_image),image.mode)

        filename = 'temp/encoded.' + str(image.format).lower()

        self.encrypted_img = img

        img.save(filename)

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
                    'Inserte su clave para desencriptar',
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