from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from collections import OrderedDict
from visualisation.ModelPage import Ui_MainWindow
from visualisation.label_dictionary import Model_Page_func
from pathlib import Path
from functionality import encryption_func
import sys, platform, subprocess, ntpath, main, os
import pickle


class ModelPageFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ModelPageFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.encryp_key_path = ("", "")
        self.config_file_path = ("", "")
        self.key_filepath2 = ""
        self.model_direc = ""
        self.seckey = None
        self.direc_list = []
        self.file_list = []
        self.selpath = []
        self.index = []
        self.counter = 0
        self.decryption_process = 0
        self.pushButton_5.clicked.connect(self.return_page)
        #self.pushButton_2.clicked.connect(self.select_encrypted_key)
        self.pushButton_2.clicked.connect(self.load_config_sig_verification)
        self.pushButton.clicked.connect(self.choose_modelfiles_direc)
        self.pushButton_4.clicked.connect(self.decrypt_models)
        self.pushButton_3.clicked.connect(self.pick_key_filepath2)
        self.pushButton_6.clicked.connect(self.show_decrypt_files)
        self.pushButton_7.clicked.connect(self.secure_addition_page)

    def return_page(self):
        self.Choose_Page_Frame = main.ChoosePageFunctionality()
        self.Choose_Page_Frame.show()
        self.close()

    def secure_addition_page(self):
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



    def load_config_sig_verification(self):
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
                self.label_2.setText("Train-Config file got successfully loaded")
            except:
                self.label_2.setText("Error while loading Train-Config. Check your Input again.")

            try:
                encryption_func.verify_digital_signature(config)
                self.label_2.setText("Train-Config file got successfully loaded & All signatures are valid")
            except:
                self.label_2.setText("During the verification of the digital signatures did occur an mismatch error")

            try:
                encry_sym_key = bytes.fromhex(config["user_encrypted_sym_key"])
                self.encryp_key_path = encry_sym_key
                self.label_2.setText("Train-Config file got successfully loaded & All signatures are valid & encrypted symmetric key got loaded")
            except:
                self.label_2.setText(
                    "Encrypted Symmetric Key could not be transferred from the Train-Config. Please try again.")



    def pick_key_filepath2(self):
        """
        Saves path of private_key in a global variable through file system selection
        :param
        :return:
        """
        file_dialog = QtWidgets.QFileDialog(self)
        keyfile2 = file_dialog.getOpenFileName(None, "Window Name", "")
        self.key_filepath2 = keyfile2[0]

        try:
            sk1 = encryption_func.load_private_key(self.key_filepath2)
        except:
            self.label_3.setText(Model_Page_func["pk_except"])
        else:

            if sk1 == "invalid":
                self.label_3.setText(Model_Page_func["pk_error_label"])
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Invalid private key")
                error_dialog.showMessage(
                    Model_Page_func["pk_error_msg"])
                error_dialog.exec_()
            else:
                self.seckey = sk1
                print("PrivateKey : ", self.seckey)
                self.label_3.setText(
                    Model_Page_func["pk_suc_label"] + self.key_filepath2)

    def walklevel(self, some_dir, level=1):
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
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.model_direc = choosen_direc
        self.direc_list = []
        self.listWidget.clear()
        self.selpath = []
        self.counter += 1
        self.label_5.setText(Model_Page_func["model_label"])
        del self.index[:]

        if self.model_direc == "":
            self.label.setText(Model_Page_func["no_direc_label"])
        else:
            for id in list(self.walklevel(self.model_direc, 1))[0][2]:
                self.direc_list.append(id)

        self.direc_list = sorted(self.direc_list, key=str.lower)
        print("directory list", self.direc_list)

        if self.model_direc != "":

            self.label.setText(Model_Page_func["dir_label"] + self.model_direc)
            self.label_6.setText(Model_Page_func["dir_label2"])

            for name in self.direc_list:
                self.listWidget.addItem(name)

            if self.counter == 1:
                self.listWidget.itemClicked.connect(self.on_click_listbox)
            else:
                None
        else:
            self.label.setText(Model_Page_func["dir_err_label"])

    def walk_dir(self, model_direc):
        """
        walks the specified directory root and returns a list of paths to these files
        :param directory to walk through
        :return: list of paths to each file in chosen directory
        """
        file_list = []
        towalk = [model_direc]
        while towalk:
            root_dir = towalk.pop()
            for path in os.listdir(model_direc):
                if os.path.isdir(os.path.join(model_direc, path)):
                    continue
                else:
                    full_path = os.path.join(model_direc, path)
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
        print("index list1",self.index)
        self.file_list = self.walk_dir(self.model_direc)
        if self.listWidget.currentRow() not in self.index:
           self.index.append(self.listWidget.currentRow())
        elif self.listWidget.currentRow() in self.index:
            self.index.remove(self.listWidget.currentRow())

        print("index list2", self.index)

        if len(self.index) == 0:
            self.label_5.setText(Model_Page_func["model_label"])
        else:
            self.selpath = [self.file_list[x] for x in self.index]
            print("selpath", self.selpath)
            model_string = "Selected models:"
            for path in self.selpath:
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
        selected_models = self.selpath

        if self.pk1 is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Missing Private Key")
            error_dialog.showMessage(Model_Page_func["missing_pk_msg"])
            error_dialog.exec_()
        else:
            try:
                encr_key = self.encryp_key_path
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("No symmetric key selected")
                error_dialog.showMessage(Model_Page_func["missing_symk_msg"])
                error_dialog.exec_()
            else:
                try:
                    decrypted_sym_key = encryption_func.decrypt_symmetric_key(encr_key, self.pk1)
                    print("sym key decrypted")
                except:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.setWindowTitle("Invalid private key selected")
                    error_dialog.showMessage(
                        Model_Page_func["mismatch_pk"])
                    error_dialog.exec_()
                else:
                    try:
                        file_encryptor = encryption_func.FileEncryptor(decrypted_sym_key)
                        decrypted_models = encryption_func.decrypt_models(selected_models, decrypted_sym_key)
                        print("models decrypted_1")
                        #print(decrypted_models[0])
                    except:
                        error_dialog = QtWidgets.QErrorMessage()
                        error_dialog.setWindowTitle("Wrong symmetric key selected")
                        error_dialog.showMessage(
                            Model_Page_func["mismatch_symk"])
                        error_dialog.exec_()
                    else:

                        print("models decrypted")
                        try:
                            for i in range(len(selected_models)):
                                path_file = os.path.split(selected_models[i])
                                save_name = path_file[0] + '/decrypted_'
                                print(save_name)
                                if '.pkl' in selected_models[i]:
                                    print("1st case")
                                    save_name += path_file[1][:-3] + 'txt'
                                    with open(save_name, "w") as decr_model:
                                        decr_model.write(str(pickle.loads(decrypted_models[i])))
                                        print("file written 1")
                                elif ".pdf" in selected_models[i]:
                                    print("2nd case")
                                    save_name += path_file[1][:-3] + 'pdf'
                                    with open(save_name, "wb") as decr_model:
                                        decr_model.write(decrypted_models[i])
                                        print("file written 2")
                                elif ".png" in selected_models[i]:
                                    print("3rd case")
                                    save_name += path_file[1][:-3] + 'png'
                                    with open(save_name, "wb") as decr_model:
                                        decr_model.write(decrypted_models[i])
                                        print("file written 3")
                        except:
                            error_dialog = QtWidgets.QErrorMessage()
                            error_dialog.setWindowTitle("Error during saving process of decrypted files")
                        self.decryption_process = 1
                        self.label_5.setText(Model_Page_func["decry_succ"])

    def show_decrypt_files(self):
        """
        opens directory in explorer where the decrypted modelfiles are saved
        :param
        :return:
        """
        if self.decryption_process == 1:

            if platform.system() == "Windows":
                os.startfile(self.model_direc)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", self.model_direc])
            else:
                subprocess.Popen(["xdg-open", self.model_direc])

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