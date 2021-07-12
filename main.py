
from PyQt5 import QtCore, QtGui, QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from visualisation.ChoosePage import Ui_MainWindow
from functionality import ModelPageFunctionality
from functionality import SecureAddtionFunctionality
from functionality import primes
from functionality.primes import PrivateKey, PublicKey
from functionality.SecurityValuesFunctionality import SecurityValuesFunctionality
from functionality.SecureAddtionFunctionality import SecureAdditionFunctionality

import sys, platform
from visualisation.label_dictionary import *
#import qdarkstyle
#import qdarkgraystyle


class ChoosePageFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(ChoosePageFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.switch_to_security)
        self.pushButton_2.clicked.connect(self.switch_to_model)
        self.pushButton_3.clicked.connect(self.switch_to_SecureAddition)
        self.label5_text = main_func_labels["Copyright"]
        self.label_5.setText(self.label5_text)
        self.label_5.linkActivated.connect(self.link_handler)

    def switch_to_model(self):
        self.ModelPage_Frame = ModelPageFunctionality.ModelPageFunctionality()
        self.ModelPage_Frame.show()
        self.close()

    def switch_to_security(self):
        self.SecurityValues_Frame = SecurityValuesFunctionality()
        self.SecurityValues_Frame.show()
        self.close()

    def switch_to_SecureAddition(self):
        self.SecureAddition_Frame = SecureAdditionFunctionality()
        self.SecureAddition_Frame.show()
        self.close()

    @staticmethod
    def link_handler():
        text = main_func_labels["MIT License"]
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Copyright")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyleSheet(open("./visualisation/darkorange.stylesheet").read())
    if platform.system() == "Windows" or platform.system() == "Darwin":
       app.setStyle('Fusion')
    else:
        None
    nextGui = ChoosePageFunctionality()
    nextGui.show()
    sys.exit(app.exec_())