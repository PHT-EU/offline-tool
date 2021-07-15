from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from collections import OrderedDict
from visualisation.ModelPage import Ui_MainWindow
from visualisation.label_dictionary import Model_Page_func
from pathlib import Path
from functionality import encryption_func
import sys, platform, subprocess, ntpath, main, os
import pickle
from cryptography.exceptions import InvalidSignature


class ModelPageFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ModelPageFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.encrypted_key = None
        self.config_file_path = ("", "")
        self.model_dir = ""
        self.private_key_path = ""
        self.private_key = None
        self.dir_list = []
        self.file_list = []
        self.selected_path = []
        self.index_list = []
        self.counter = 0
        self.decryption_process = 0

        self.pushButton_5.clicked.connect(self.move_return_page)
        self.pushButton_2.clicked.connect(self.load_train_config)
        self.pushButton.clicked.connect(self.choose_modelfiles_direc)
        self.pushButton_4.clicked.connect(self.decrypt_models)
        self.pushButton_3.clicked.connect(self.select_private_key)
        self.pushButton_6.clicked.connect(self.show_decrypted_files)
        self.pushButton_7.clicked.connect(self.move_secure_addition_page)

    def move_return_page(self):
        self.Choose_Page_Frame = main.ChoosePageFunctionality()
        self.Choose_Page_Frame.show()
        self.close()

    def move_secure_addition_page(self):
        self.Secure_Addition_Page_Frame = main.SecureAdditionFunctionality()
        self.Secure_Addition_Page_Frame.show()
        self.close()

    def select_encrypted_key(self):
        """
        Saves path of encrypted_symmetric_key in a global variable through file system selection
        :param
        :return:
        """
        keyfile1 = QtWidgets.QFileDialog.getOpenFileName(self)
        self.encryp_key_path = keyfile1[0]

        if self.encryp_key_path != "":
            self.label_2.setText(Model_Page_func["encry_key_func"] + self.encryp_key_path)
            print("Encrypted Key Path : ", self.encryp_key_path)
        else:
            self.label_2.setText(Model_Page_func["encry_key_error"])

    def load_train_config(self):
        """
        Saves path of train_config.json in a global variable through file system selection
        Then it verifies the digital signature with the public keys given in the config file
        :param
        :return:
        """

        config_file = QtWidgets.QFileDialog.getOpenFileName(self)
        self.config_file_path = config_file[0]

        if self.config_file_path != "":

            try:
                config = encryption_func.load_config(self.config_file_path)
                self.label_2.setText(Model_Page_func["config_succ_load"])

                try:
                    encryption_func.verify_digital_signature(config)
                    self.label_2.setText(Model_Page_func["config_succ_sign"])
                except ValueError as e:
                    self.label_2.setText(f"Error verifying signature:\n {e}")
                except InvalidSignature as e:
                    self.label_2.setText(f"Error verifying signature:\n {e}")
                except:
                    self.label_2.setText(Model_Page_func["config_failed_sign"])
                    return None

            except:
                self.label_2.setText(Model_Page_func["config_failed_load"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Error while loading config file")
                error_dialog.showMessage(
                    Model_Page_func["config_failed_load"])
                error_dialog.exec_()
                return None
            try:
                self.encrypted_key = bytes.fromhex(config["user_encrypted_sym_key"])
                self.label_2.setText(
                    Model_Page_func["config_encry_key_succ"])
            except:
                self.label_2.setText(
                    Model_Page_func["config_encry_key_failed"])

    def select_private_key(self):
        """
        Saves path of private_key in a global variable through file system selection
        :param
        :return:
        """

        file_dialog = QtWidgets.QFileDialog(self)
        keyfile2 = file_dialog.getOpenFileName(None, "Window Name", "")
        self.private_key_path = keyfile2[0]
        if keyfile2[0] == "":
            return None
        private_key_psw = QtWidgets.QInputDialog.getText(self, "Password for Private Key",
                                                         "Enter the existing password for your Private Key:")

        try:
            self.private_key = encryption_func.load_private_key(self.private_key_path, private_key_psw)
        except:
            self.label_3.setText("Error while loading private key: Invalid Input")
        else:
            if self.private_key == "invalid":
                self.label_3.setText(Model_Page_func["pk_error_label"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Error while loading Private key")
                error_dialog.showMessage(
                    Model_Page_func["pk_error_msg"])
                error_dialog.exec_()
            elif self.private_key == "wrong_password":
                self.label_3.setText(Model_Page_func["pk_error_label_2"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Error while loading Private key")
                error_dialog.showMessage(
                    Model_Page_func["pk_error_msg_2"])
                error_dialog.exec_()
            else:
                print("PrivateKey : ", self.private_key)
                self.label_3.setText(
                    Model_Page_func["pk_suc_label"] + self.private_key_path)

    def filter_out_dir(self, some_dir, level=1):
        """
        filter out file-paths that lead to other directories
        :param
        :return:
        """
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def choose_modelfiles_direc(self):
        """
        lists all files in a chosen directory with links to respective paths in a PyQT-ListWidget
        when files are selected the corresponding paths are selected and ready for decryption
        :param
        :return:
        """
        chosen_dir = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.model_dir = chosen_dir
        self.dir_list = []
        self.listWidget.clear()
        self.selected_path = []
        self.counter += 1
        self.label_5.setText(Model_Page_func["model_label"])
        del self.index_list[:]

        if self.model_dir == "":
            self.label.setText(Model_Page_func["no_direc_label"])
        else:
            for id in list(self.filter_out_dir(self.model_dir, 1))[0][2]:
                self.dir_list.append(id)

        self.dir_list = sorted(self.dir_list, key=str.lower)

        if self.model_dir != "":

            self.label.setText(Model_Page_func["dir_label"] + self.model_dir)
            self.label_6.setText(Model_Page_func["dir_label2"])

            for name in self.dir_list:
                self.listWidget.addItem(name)

            if self.counter == 1:
                self.listWidget.itemClicked.connect(self.on_click_listbox)
            else:
                None
        else:
            self.label.setText(Model_Page_func["dir_err_label"])

    def get_filepaths_of_dir(self, model_dir):
        """
        walks the specified directory root and returns a list of paths to these files
        :param directory to walk through
        :return: list of paths to each file in chosen directory
        """
        file_list = []
        towalk = [model_dir]
        while towalk:
            root_dir = towalk.pop()
            for path in os.listdir(model_dir):
                if os.path.isdir(os.path.join(model_dir, path)):
                    continue
                else:
                    full_path = os.path.join(model_dir, path)
                    # create list of (filename, dir) tuples
                    file_list.append(full_path)

        file_list = sorted(file_list, key=str.lower)
        return file_list

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def on_click_listbox(self):
        """
        saves path to files in a list that were clicked on in the PyQT-ListWidget
        :param
        :return:
        """

        self.file_list = self.get_filepaths_of_dir(self.model_dir)
        if self.listWidget.currentRow() not in self.index_list:
            self.index_list.append(self.listWidget.currentRow())
        elif self.listWidget.currentRow() in self.index_list:
            self.index_list.remove(self.listWidget.currentRow())


        if len(self.index_list) == 0:
            self.label_5.setText(Model_Page_func["model_label"])
        else:
            self.selected_path = [self.file_list[x] for x in self.index_list]
            model_string = "Selected models:"
            for path in self.selected_path:
                path = self.path_leaf(path)
                model_string += ("\n" + "\n" + path)

            self.label_5.setText(model_string)

    def decrypt_models(self):
        """
        decrypts the before selected encrypted_symmetric_key with the chosen private_key and raises error if mismatch
        then decrypts the selected files in the PyQT-ListWidget and writes the decrypted file into the same directory
        :param
        :return: decrypted models in .txt format
        """
        selected_models = self.selected_path

        if self.private_key is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Missing Private Key")
            error_dialog.showMessage(Model_Page_func["missing_pk_msg"])
            error_dialog.exec_()
        elif self.encrypted_key == None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Missing Encrypted Key")
            error_dialog.showMessage("Missing Encrypted Key. Please load your Config file before decrypting.")
            error_dialog.exec_()
        else:
            try:
                decrypted_sym_key = encryption_func.decrypt_symmetric_key(self.encrypted_key, self.private_key)
                file_encryptor = encryption_func.FileEncryptor(decrypted_sym_key)
                decrypted_models = encryption_func.decrypt_models(selected_models, decrypted_sym_key)
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Invalid Private Key selected")
                error_dialog.showMessage(
                    Model_Page_func["mismatch_pk"])
                error_dialog.exec_()
                self.label_5.setText(Model_Page_func["mismatch_pk"])
                return None
            try:
                for i in range(len(selected_models)):
                    path_file = os.path.split(selected_models[i])
                    save_name = path_file[0] + '/decrypted_' + path_file[1][:]
                    with open(save_name, "wb") as decr_model:
                        decr_model.write(decrypted_models[i])
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Error Saving Decrypted Files")
                error_dialog.showMessage("Error while trying to save the decrypted files locally.")
                return None
            else:
                self.decryption_process = 1
                self.label_5.setText(Model_Page_func["decry_succ"])

    def show_decrypted_files(self):
        """
        opens directory in explorer where the decrypted modelfiles are saved
        :param
        :return:
        """
        if self.decryption_process == 1:

            if platform.system() == "Windows":
                os.startfile(self.model_dir)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", self.model_dir])
            else:
                subprocess.Popen(["xdg-open", self.model_dir])

        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("No Decryption")
            error_dialog.showMessage(Model_Page_func["show_models_err"])
            error_dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if platform.system() == "Windows" or platform.system() == "Darwin":
        app.setStyle('Fusion')
    else:
        None
    nextGui = ModelPageFunctionality()
    nextGui.show()
    sys.exit(app.exec_())
