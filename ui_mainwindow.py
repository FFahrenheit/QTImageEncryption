# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(630, 390)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.original_image = QLabel(self.centralwidget)
        self.original_image.setObjectName(u"original_image")
        self.original_image.setGeometry(QRect(190, 30, 240, 240))
        self.original_image.setFrameShape(QFrame.WinPanel)
        self.original_image.setFrameShadow(QFrame.Sunken)
        self.load_image = QPushButton(self.centralwidget)
        self.load_image.setObjectName(u"load_image")
        self.load_image.setGeometry(QRect(280, 300, 101, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 630, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.original_image.setText(QCoreApplication.translate("MainWindow", u"Original image", None))
        self.load_image.setText(QCoreApplication.translate("MainWindow", u"Cargar imagen", None))
    # retranslateUi

