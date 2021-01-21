from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from visualisation.SecureAddition import Ui_MainWindow
from functionality import primes
import sys, platform, subprocess, ntpath, main, os, re
import pickle
from visualisation.label_dictionary import Security_Page_func


class SecureAdditionFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SecureAdditionFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.folder_path = ""
        self.key_filepath = ""
        self.private_key_name = ""
        self.public_key_name = ""
        self.pk = ""
        self.pubkey_filepath = ""
        self.pushButton_5.clicked.connect(self.return_page)
        self.pushButton.clicked.connect(self.generate_key_pair)
        self.pushButton_2.clicked.connect(self.pick_key_filepath)
        self.pushButton_3.clicked.connect(self.decrypt)



    def browse_direc(self):
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.folder_path = choosen_direc
        print(self.folder_path)



    def generate_key_pair(self):
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.folder_path = choosen_direc

        if self.folder_path != "":
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
                    self.private_key_name = choosen_direc + '/' + private_key_name[0]
                    self.public_key_name = choosen_direc + '/' + private_key_name[0]
                    print(self.public_key_name + "_pk.p")
                    print(self.private_key_name + "_sk.p")

                sk, pk = primes.generate_keypair(128)
                print(type(sk))
                print(sk)
                print(type(pk.n))
                pk = str(pk.n)
                print(pk)
                pickle.dump(sk, open(self.private_key_name + "_sk.p", "wb"))
                #pickle.dump(pk, open(self.private_key_name + "_pk.p", "wb"))
                with open(self.private_key_name + "_pk.p", "w") as pub_key:
                    pub_key.write(pk)
                self.label.setText(Security_Page_func["key_succ"] + choosen_direc)

        else:
            self.label.setText(Security_Page_func["key_err"])


    def pick_key_filepath(self):
        """
        Choose a key-file in the corresponding directory that will then be saved into a global variable
        :param
        :return:
        """
        file_dialog = QtWidgets.QFileDialog(self)
        keyfile = file_dialog.getOpenFileName(None, "Window Name", "")
        self.key_filepath = keyfile[0]
        self.pubkey_filepath = self.key_filepath.split("_")
        self.pubkey_filepath = "_".join(self.pubkey_filepath[:-1]) + "_pk.p"
        print(self.pubkey_filepath)

        try:
            pk = pickle.load(open(self.key_filepath, "rb"))
            print("OK1")
            pub_key = open(self.pubkey_filepath, "r")
            self.pubkey_filepath = pub_key.read()
            print(self.pubkey_filepath)
            print("OK2")
        except:
            self.label_2.setText(Security_Page_func["pick_key_label"])
        else:
            if pk == "invalid":
                self.label_2.setText(Security_Page_func["invalid_key"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Invalid private key")
                error_dialog.showMessage(
                    Security_Page_func["invalid_key_err"])
                error_dialog.exec_()
            else:
                self.pk = pk
                self.label_2.setText(
                    Security_Page_func["load_key"] + self.key_filepath)


    def decrypt(self):
        """
        Signs a given hash (SHA512-format) with the before loaded private key
        :param
        :return: signed-hash in hex-format
        """
        encry_string = self.textEdit.toPlainText().rstrip().lstrip()


        if self.pk is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Private key missing")
            error_dialog.showMessage(Security_Page_func["no_pk_hash_err"])
            error_dialog.exec_()
        elif len(encry_string) > 1:
            #self.pubkey_filepath = int(self.pubkey_filepath)
            #print(self.pubkey_filepath)
            #print(int(encry_string))

            self.pubkey_filepath = primes.PublicKey.from_n(int(self.pubkey_filepath))

            result = primes.decrypt(self.pk, self.pubkey_filepath, int(encry_string))
            self.textEdit_2.setText("Number of patients decrypted: {}".format(result))
            self.label_5.setText("Decryption was successfull")
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Invalid format")
            error_dialog.showMessage(Security_Page_func["invalid_hash"])
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