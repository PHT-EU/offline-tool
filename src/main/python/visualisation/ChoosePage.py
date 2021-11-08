# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dynamic_ChoosePage2.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from visualisation.label_dictionary import choose_page_labels
import qdarkstyle
import os, sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 710)
        MainWindow.setMinimumSize(QtCore.QSize(638, 587))
        self.setStyleSheet("background-color: #e6e6e6;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setText("")
        #self.appctxt = ApplicationContext()
        #self.image_path = self.appctxt.get_resource('./visualisation/PHT_offline-tool.png')
        #self.label_3.setPixmap(QtGui.QPixmap(self.image_path))

        # self.label_3.setPixmap(QtGui.QPixmap("./visualisation/PHT_offline-tool.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 3)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.frame_3)
        self.pushButton.setMinimumSize(QtCore.QSize(235, 50))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setMinimumSize(QtCore.QSize(235, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_3.setMinimumSize(QtCore.QSize(255, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(361, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 895, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.setStyleSheet("font: 14px Arial")
        self.label_2.setStyleSheet("font: 14px Arial")
        self.pushButton_2.setStyleSheet("font: 14px Arial")
        self.label.setStyleSheet("font: 14px Arial")
        self.pushButton_3.setStyleSheet("font: 14px Arial")
        self.label_6.setStyleSheet("font: 14px Arial")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PHT offline tool"))
        self.label_2.setText(_translate("MainWindow", "Choose your model files and decrypt them using private and encrypted symmetric key"))
        self.pushButton.setText(_translate("MainWindow", "Security Values"))
        self.label.setText(_translate("MainWindow", "Generate your private and public keys aswell as hash signing for submitting valid trains"))
        self.pushButton_2.setText(_translate("MainWindow", "Model Page"))
        self.pushButton_3.setText(_translate("MainWindow", "Secure Addition"))
        self.label_6.setText(_translate("MainWindow", "Key pair creation and decryption of results"))
        self.label_4.setText(_translate("MainWindow", "<a href=\"https://personalhealthtrain.de\"><font color=black>PHT-TBI</font></a>"))
        self.label_5.setText(_translate("MainWindow", "Created by Felix Bötte"))




#self.pht_link ="<a href=\"https://pht.difuture.de\"><font color=black>pht.difuture.de</font></a>"


        self.pushButton.setStyleSheet("font: 14px Arial")
        self.label_2.setStyleSheet("font: 14px Arial")
        self.pushButton_2.setStyleSheet("font: 14px Arial")
        self.label.setStyleSheet("font: 14px Arial")

        '''self.appctxt = ApplicationContext()
        self.image_path = self.appctxt.get_resource('PHT_offline-tool.png')
        self.label_3.setPixmap(QtGui.QPixmap(self.image_path)) '''

        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'images', 'PHT_offline-tool.png')))
        #self.label_3.setPixmap(QtGui.QPixmap("../resources/base/images/PHT_offline-tool.png"))
        self.label_3.setScaledContents(True)
