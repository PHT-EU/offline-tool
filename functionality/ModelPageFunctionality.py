from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from collections import OrderedDict
from visualisation.ModelPage import Ui_MainWindow
from pathlib import Path
from functionality import encryption_func
import sys, platform, subprocess, ntpath, main, os



class ModelPageFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ModelPageFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.encryp_key_path = ("", "")
        self.key_filepath2 = ""
        self.model_direc = ""
        self.pk1 = None
        self.direc_list = []
        self.file_list = []
        self.selpath = []
        self.index = []
        self.counter = 0
        self.decryption_process = 0
        self.pushButton_5.clicked.connect(self.return_page)
        self.pushButton_2.clicked.connect(self.select_encrypted_key)
        self.pushButton.clicked.connect(self.choose_modelfiles_direc)
        self.pushButton_4.clicked.connect(self.decrypt_models)
        self.pushButton_3.clicked.connect(self.pick_key_filepath2)
        self.pushButton_6.clicked.connect(self.show_decrypt_files)

    def return_page(self):
        self.Choose_Page_Frame = main.ChoosePageFunctionality()
        self.Choose_Page_Frame.show()
        self.close()

    def select_encrypted_key(self):
        keyfile1 = QtWidgets.QFileDialog.getOpenFileName(self)
        self.encryp_key_path = keyfile1[0]

        if self.encryp_key_path != "":
            self.label_2.setText("Chosen encrypted symmetric key loaded successfully:" + "\n" + "\n" + self.encryp_key_path)
            print(self.encryp_key_path)
        else:
            self.label_2.setText("You haven't selected a valid key file")

    def pick_key_filepath2(self):
        file_dialog = QtWidgets.QFileDialog(self)
        keyfile2 = file_dialog.getOpenFileName(None, "Window Name", "", "pem(*_sk.pem)")
        self.key_filepath2 = keyfile2[0]

        try:
            pk1 = encryption_func.load_private_key(self.key_filepath2)
        except:
            self.label_3.setText("Please select a key file")
        else:

            if pk1 == "invalid":
                self.label_3.setText("You haven't selected a valid key file")
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("Invalid private key")
                error_dialog.showMessage(
                    "The selected private key is invalid. Choose a valid key or generate a new one")
                error_dialog.exec_()
            else:
                self.pk1 = pk1
                self.label_3.setText(
                    "The selected private key loaded successfully:" + "\n" + "\n" + self.key_filepath2)

    def walklevel(self, some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def choose_modelfiles_direc(self):
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.model_direc = choosen_direc
        self.direc_list = []
        self.listWidget.clear()
        self.selpath = []
        self.counter += 1
        self.label_5.setText("No models selected" + "\n" + "\n" + "Please click on the file(s) to select them")
        del self.index[:]

        if self.model_direc == "":
            self.label.setText("No directory selected yet")
        else:
            for id in list(self.walklevel(self.model_direc, 1))[0][2]:
                self.direc_list.append(id)

        self.direc_list = sorted(self.direc_list, key=str.lower)
        print("directory list", self.direc_list)

        if self.model_direc != "":

            self.label.setText("Selected directory:" + "\n" + "\n" + self.model_direc)
            self.label_6.setText("Please click one the files to select them")

            for name in self.direc_list:
                self.listWidget.addItem(name)

            if self.counter == 1:
                self.listWidget.itemClicked.connect(self.on_click_listbox)
            else:
                None
        else:
            self.label.setText("Please select a valid directory")

    def walk_dir(self, model_direc):
        # walks the specified directory root and returns a list of paths to these files
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
        print("index list1",self.index)
        self.file_list = self.walk_dir(self.model_direc)
        if self.listWidget.currentRow() not in self.index:
           self.index.append(self.listWidget.currentRow())
        elif self.listWidget.currentRow() in self.index:
            self.index.remove(self.listWidget.currentRow())

        print("index list2", self.index)

        if len(self.index) == 0:
            self.label_5.setText("No models selected" + "\n" + "\n" + "Please click on the file(s) to select them")
        else:
            self.selpath = [self.file_list[x] for x in self.index]
            print("selpath", self.selpath)
            model_string = "Selected models:"
            for path in self.selpath:
                path = self.path_leaf(path)
                model_string += ("\n" + "\n" + path)

            self.label_5.setText(model_string)



    def decrypt_models(self):

        selected_models = self.selpath

        if self.pk1 is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Missing Private Key")
            error_dialog.showMessage("No private key selected to decrypt the models. Please select one.")
            error_dialog.exec_()
        else:
            try:
                with open(self.encryp_key_path, "rb") as encr_sym_key:
                    encr_key = encr_sym_key.read()
                    print("sym key read")
            except:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.setWindowTitle("No symmetric key selected")
                error_dialog.showMessage("You haven't selected a symmetric key. Please define one above")
                error_dialog.exec_()
            else:
                try:
                    sym_key = encryption_func.decrypt_symmetric_key(encr_key, self.pk1)
                    print("sym key decrypted")
                except:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.setWindowTitle("Invalid private key selected")
                    error_dialog.showMessage(
                        "You haven't selected a matching private key for the encrypted models")
                    error_dialog.exec_()
                else:
                    try:
                        decrypted_models = encryption_func.decrypt_models(selected_models, sym_key)
                    except:
                        error_dialog = QtWidgets.QErrorMessage()
                        error_dialog.setWindowTitle("Wrong symmetric key selected")
                        error_dialog.showMessage(
                            "You haven't selected a matching symmetric key for the encrypted models")
                        error_dialog.exec_()
                    else:

                        print("models decrypted")

                        for i in range(len(selected_models)):
                            with open(selected_models[i], "w") as decr_model:
                                decr_model.write(str(decrypted_models[i]))
                        self.decryption_process = 1
                        self.label_5.setText("Selected models have been successfully decrypted ")

    def show_decrypt_files(self):
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
            error_dialog.showMessage("No files decrypted yet.",
                                     "Please select the models in your selected directory and decrypt them")
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