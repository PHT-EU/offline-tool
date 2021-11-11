from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from visualisation.SecureAddition import Ui_MainWindow
from functionality import primes
import sys, platform, subprocess, ntpath, main, os, re
import pickle
from visualisation.label_dictionary import Security_Page_func


public_key_file_ = None
public_key_filepath_ = None
private_key_file_ = None
private_key_filepath_ = None



class SecureAdditionFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SecureAdditionFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.key_dir = ""
        self.private_key_filepath = ""
        self.public_key_filepath = ""
        self.private_key_name = ""
        self.public_key_name = ""
        self.private_key = ""
        self.public_key = ""
        self.pushButton_5.clicked.connect(self.return_page)
        self.pushButton.clicked.connect(self.generate_key_pair)
        self.pushButton_2.clicked.connect(self.pick_private_key_filepath)
        self.pushButton_3.clicked.connect(self.decrypt)

        if private_key_file_ is not None:
            self.label_2.setText(Security_Page_func["load_key"] + private_key_filepath_)



    def browse_direc(self):
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.keydir_path = choosen_direc
        print(self.keydir_path)



    def generate_key_pair(self):
        chosen_dir = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.key_dir = chosen_dir

        if self.key_dir != "":
            private_key_name = QtWidgets.QInputDialog.getText(self, Security_Page_func["key_name_title"],
                                                              Security_Page_func["key_name_msg"])

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
                    self.private_key_name = chosen_dir + '/' + private_key_name[0]
                    self.public_key_name = chosen_dir + '/' + private_key_name[0]

                try:
                    private_key, public_key = primes.generate_keypair(128)
                    public_key = str(public_key.n)

                    pickle.dump(private_key, open(self.private_key_name + "_sk.p", "wb"))
                    with open(self.private_key_name + "_pk.p", "w") as key:
                        key.write(public_key)
                    self.label.setText(Security_Page_func["key_succ"] + chosen_dir)
                except:
                    self.label.setText("Error while generating keys, Please try again.")

        else:
            self.label.setText(Security_Page_func["key_err"])


    def pick_private_key_filepath(self):
        """
        Choose a key-file in the corresponding directory that will then be saved into a global variable
        :param
        :return:
        """
        global public_key_file_
        global private_key_file_
        global public_key_filepath_
        global private_key_filepath_


        file_dialog = QtWidgets.QFileDialog(self)
        private_keyfile = file_dialog.getOpenFileName(None, "Select Private Key", "", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.private_key_filepath = private_keyfile[0]
        private_key_filepath_ = private_keyfile[0]

        self.public_key_filepath = self.private_key_filepath.split("_")
        self.public_key_filepath = "_".join(self.public_key_filepath[:-1]) + "_pk.p"


        public_key_filepath_ = self.public_key_filepath
        print("Private Keyfile Filepath: {}".format(self.private_key_filepath))
        print("Public Key Filepath {}".format(self.public_key_filepath))


        self.private_key = pickle.load(open(self.private_key_filepath, "rb"))
        private_key_file_ = self.private_key
        try:
            self.public_key = open(self.public_key_filepath, "r").read()
            public_key_file_ = self.public_key
        except:
            self.public_key = pickle.load(open(self.public_key_filepath, "rb")).n
            public_key_file_ = self.public_key
        else:
            if self.private_key == "invalid":
                self.label_2.setText(Security_Page_func["invalid_key"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Invalid private key")
                error_dialog.showMessage(
                    Security_Page_func["invalid_key_err"])
                error_dialog.exec_()
            else:
                self.label_2.setText(
                    Security_Page_func["load_key"] + self.private_key_filepath)


    def decrypt(self):
        """
        Signs a given hash (SHA512-format) with the before loaded private key
        :param
        :return: signed-hash in hex-format
        """
        global public_key_file_
        global private_key_file_

        encrypted_string = self.textEdit.toPlainText().rstrip().lstrip()


        if private_key_file_ is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Private key missing")
            error_dialog.showMessage(Security_Page_func["no_pk_hash_err"])
            error_dialog.exec_()
        elif len(encrypted_string) > 1:

            try:
                public_key = int(public_key_file_)
                result = primes.decrypt_int(private_key_file_, public_key, int(encrypted_string))
                self.textEdit_2.setText("Decrypted homomorphic encrypted value: {}".format(result))
                self.label_5.setText("Decryption was successfull")
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Invalid format")
                error_dialog.showMessage("Encrypted homomorphic value not in the right format. Please check your input.")
                error_dialog.exec_()

        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Invalid format")
            error_dialog.showMessage("Encrypted homomorphic value not in the right format. Please check your input.")
            error_dialog.exec_()


    def return_page(self):
        self.Choose_Page_Frame = main.ChoosePageFunctionality()
        self.Choose_Page_Frame.show()
        self.close()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if platform.system() == "Windows" or platform.system() == "Darwin":
        app.setStyle('Fusion')
    else:
        None
    nextGui = SecureAdditionFunctionality()
    nextGui.show()
    sys.exit(app.exec_())