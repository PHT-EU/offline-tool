from PyQt5 import QtCore, QtGui, QtWidgets
from numpy.core.defchararray import upper
from PyQt5.Qt import QApplication, QClipboard
from visualisation.SecurityValues import Ui_MainWindow
#import ModelPageFunctionality
from functionality import encryption_func
import main, platform
from visualisation.label_dictionary import Security_Page_func, Model_Page_func
import re

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
#from fbs_runtime.application_context.PyQt5 import ApplicationContext


class SecurityValuesFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(SecurityValuesFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.dir_path = ""
        self.private_key_filepath = ""
        self.private_key_name = ""
        self.public_key_name = ""
        self.private_key = None
        self.hash_text = ""
        self.pushButton_2.clicked.connect(self.pick_private_key_filepath)
        self.pushButton_3.clicked.connect(self.sign_hash)
        self.pushButton.clicked.connect(self.generate_private_key)
        self.pushButton_5.clicked.connect(self.return_page)
        self.pushButton_4.clicked.connect(self.copy_hash)

    def browse_direc(self):
        chosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.dir_path = chosen_direc

    def generate_private_key(self):
        """
        Choose a directory where a private_key and public_key are then stored
        Then choose a name for the key_pair which will have the form "name" + "_pk.pem" / "_sk.pem"
        :param
        :return:
        """
        chosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.dir_path = chosen_direc

        if self.dir_path != "":

            private_key_name = QtWidgets.QInputDialog.getText(self, Security_Page_func["key_name_title"],
                                                              Security_Page_func["key_name_msg"])

            private_key_psw = QtWidgets.QInputDialog.getText(self, "Password for Private Key",
                                                              "Enter the password for your Private Key:")

            if private_key_name[0] != "":

                while re.match(r'^[A-Za-z0-9_]+$', private_key_name[0]) is False:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.setWindowTitle("Invalid key name")
                    error_dialog.showMessage(
                        Security_Page_func["key_name_err"])
                    error_dialog.exec_()
                    private_key_name = QtWidgets.QInputDialog.getText(self, Security_Page_func["key_name_title"],
                                                                      Security_Page_func["key_name_msg"])
                else:
                    self.private_key_name = chosen_direc + '/' + private_key_name[0]
                    self.public_key_name = chosen_direc + '/' + private_key_name[0]



                try:
                    rsa_private_key, rsa_public_key = encryption_func.create_rsa_keys(private_key_psw)
                    encryption_func.store_keys(self.dir_path, rsa_private_key, rsa_public_key,  private_key_name[0])
                    self.label.setText(Security_Page_func["key_succ"] + chosen_direc)
                except:
                    self.label.setText(Security_Page_func["psw_err"])


        else:
            self.label.setText(Security_Page_func["key_err"])


    def pick_private_key_filepath(self):
        """
        Choose a key-file in the corresponding directory that will then be saved into a global variable
        :param
        :return:
        """
        file_dialog = QtWidgets.QFileDialog(self)
        keyfile = file_dialog.getOpenFileName(None, "Select Private Key", "")
        if keyfile[0] == "":
            return None
        self.private_key_filepath = keyfile[0]

        private_key_psw = QtWidgets.QInputDialog.getText(self, "Password for Private Key",
                                                         "Enter the existing password for your Private Key:")

        try:
            self.private_key = encryption_func.load_private_key(self.private_key_filepath, private_key_psw)
        except:
            self.label_2.setText("Error while loading private key: Invalid Input")
        else:
            if self.private_key == "invalid":
                self.label_2.setText(Model_Page_func["pk_error_label"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Error while loading Private key")
                error_dialog.showMessage(
                    Model_Page_func["pk_error_msg"])
                error_dialog.exec_()
            elif self.private_key == "wrong_password":
                self.label_2.setText(Model_Page_func["pk_error_label_2"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Error while loading Private key")
                error_dialog.showMessage(
                    Model_Page_func["pk_error_msg_2"])
                error_dialog.exec_()
            else:
                print("PrivateKey : ", self.private_key)
                self.label_2.setText(
                    Model_Page_func["pk_suc_label"] + self.private_key_filepath)

    def sign_hash(self):
        """
        Signs a given hash (SHA512-format) with the before loaded private key
        :param
        :return: signed-hash in hex-format
        """
        hash_string = self.textEdit.toPlainText().rstrip().lstrip()

        try:
            hash_string = bytes.fromhex(hash_string)
        except:
            self.label_5.setText("Error with the hash. Please check your input.")

        if self.private_key is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Private key missing")
            error_dialog.showMessage(Security_Page_func["no_pk_hash_err"])
            error_dialog.exec_()
        elif len(hash_string) > 1:
            try:
                signature = encryption_func.sign_hash(self.private_key, hash_string)
                signature_hex = signature.hex()
                self.textEdit_2.setText(signature_hex)
                self.label_5.setText(Security_Page_func["hash_sign"])
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Invalid hash format")
                error_dialog.showMessage(Security_Page_func["invalid_hash"])
                error_dialog.exec_()
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Invalid hash format")
            error_dialog.showMessage(Security_Page_func["invalid_hash"])
            error_dialog.exec_()

    def copy_hash(self):
        """
        displays the signed-hash in hex-format in the PyQT-TextBox
        :param
        :return:
        """

        textbox_hash = self.textEdit_2.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(textbox_hash, mode=clipboard.Clipboard)

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