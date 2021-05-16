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
        MainWindow.resize(715, 420)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabBarAutoHide(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.encrypt_result = QLabel(self.tab)
        self.encrypt_result.setObjectName(u"encrypt_result")
        self.encrypt_result.setFrameShape(QFrame.WinPanel)
        self.encrypt_result.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.encrypt_result, 0, 1, 1, 1)

        self.encrypt_open = QPushButton(self.tab)
        self.encrypt_open.setObjectName(u"encrypt_open")

        self.gridLayout.addWidget(self.encrypt_open, 1, 0, 1, 1)

        self.encrypt_original = QLabel(self.tab)
        self.encrypt_original.setObjectName(u"encrypt_original")
        self.encrypt_original.setFrameShape(QFrame.WinPanel)
        self.encrypt_original.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.encrypt_original, 0, 0, 1, 1)

        self.encryption_progress = QProgressBar(self.tab)
        self.encryption_progress.setObjectName(u"encryption_progress")
        self.encryption_progress.setEnabled(True)
        self.encryption_progress.setValue(0)
        self.encryption_progress.setTextVisible(False)

        self.gridLayout.addWidget(self.encryption_progress, 2, 0, 1, 2)

        self.encrypt_save = QPushButton(self.tab)
        self.encrypt_save.setObjectName(u"encrypt_save")

        self.gridLayout.addWidget(self.encrypt_save, 1, 1, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 715, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.encrypt_result.setText(QCoreApplication.translate("MainWindow", u"Imagen encriptada", None))
        self.encrypt_open.setText(QCoreApplication.translate("MainWindow", u"Abrir imagen", None))
        self.encrypt_original.setText(QCoreApplication.translate("MainWindow", u"Imagen original", None))
        self.encrypt_save.setText(QCoreApplication.translate("MainWindow", u"Guardar imagen", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Encriptar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Desencriptar", None))
    # retranslateUi

