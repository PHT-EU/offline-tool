from PyQt5 import QtCore, QtGui, QtWidgets
from numpy.core.defchararray import upper
from PyQt5.Qt import QApplication, QClipboard
from visualisation.SecurityValues import Ui_MainWindow
#import ModelPageFunctionality
from functionality import encryption_func
import main, platform
import re

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
#from fbs_runtime.application_context.PyQt5 import ApplicationContext


class SecurityValuesFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(SecurityValuesFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.folder_path = ""
        self.key_filepath = ""
        self.private_key_name = ""
        self.public_key_name = ""
        self.pk = None
        self.hash_text = ""
        self.pushButton_2.clicked.connect(self.pick_key_filepath)
        self.pushButton_3.clicked.connect(self.sign_hash_btn)
        self.pushButton.clicked.connect(self.generate_private_key)
        self.pushButton_5.clicked.connect(self.return_page)
        self.pushButton_4.clicked.connect(self.copy_hash)

    def browse_direc(self):
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.folder_path = choosen_direc
        print(self.folder_path)

    def generate_private_key(self):
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.folder_path = choosen_direc

        if self.folder_path != "":

            private_key_name = QtWidgets.QInputDialog.getText(self, 'Generate private/public key', 'Enter a name for your private/public key:')


            while re.match(r'^[A-Za-z0-9_]+$', private_key_name[0]) is False:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Unvalid key name")
                error_dialog.showMessage(
                    "The name of your key wasn´t valid. Please use only letters or numbers")
                error_dialog.exec_()
                private_key_name = QtWidgets.QInputDialog.getText(self, 'Generate private/public key',
                                                                  'Enter a name for your private/public key:')
            else:
                self.private_key_name = choosen_direc + '/' + private_key_name[0]
                self.public_key_name = choosen_direc + '/' + private_key_name[0]
                print(self.public_key_name + "_pk.pem")
                print(self.private_key_name + "_sk.pem")



            rsa_sk, rsa_pk = encryption_func.create_rsa_keys()
            encryption_func.store_keys(self.folder_path, rsa_sk, rsa_pk,  private_key_name[0])
            self.label.setText("Keys got successfully generated to:" + "\n" + "\n" + choosen_direc)

        else:
            self.label.setText("You havent picked a valid directory")


    def pick_key_filepath(self):
        file_dialog = QtWidgets.QFileDialog(self)
        keyfile = file_dialog.getOpenFileName(None, "Window Name", "", "pem(*_sk.pem)")
        self.key_filepath = keyfile[0]

        try:
            pk = encryption_func.load_private_key(self.key_filepath)
        except:
            self.label_2.setText("You havent picked a keyfile yet")
        else:
            if pk == "unvalid":
                self.label_2.setText("You havent picked a valid keyfile")
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Unvalid private key")
                error_dialog.showMessage(
                    "The private key you selected wasn´t valid. Choose a valid key or generate a new one")
                error_dialog.exec_()
            else:
                self.pk = pk
                self.label_2.setText(
                    "Choosen private key got succesfully loaded and ready to use:" + "\n" + "\n" + self.key_filepath)

    def sign_hash_btn(self):
        hash_string = self.textEdit.toPlainText()

        if self.pk is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Missing Private Key")
            error_dialog.showMessage("There was no RSA private key selected to sign the hash. Please select and load one.")
            error_dialog.exec_()
        else:
            signature = encryption_func.sign_hash(self.pk, encryption_func.hash_string(hash_string))
            print(type(signature))
            self.textEdit_2.setText(str(signature))
            self.label_5.setText("Hash has been successfully signed and ready to use")

    def copy_hash(self):
        textboxValue2 = self.textEdit_2.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(textboxValue2, mode=clipboard.Clipboard)

    def return_page(self):
        self.Choose_Page_Frame = main.ChoosePageFunctionality()
        self.Choose_Page_Frame.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if platform.system() == "Windows" or platform.system() == "Darwin":
        app.setStyle('Fusion')
    else:
        None
    nextGui = SecurityValuesFunctionality()
    nextGui.show()
    sys.exit(app.exec_())