from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import  QFileSystemModel, QVBoxLayout, QTreeView
from visualisation.ModelPage import Ui_MainWindow
import os
import main
from functionality import encryption_func
import ntpath
import sys

# TODO see PEP 8 checks


class ModelPageFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ModelPageFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.encryp_key_path = ("", "")
        self.key_filepath2 = ""
        self.model_direc = ""
        self.pk = ""
        self.selpath = []
        self.index = []
        self.decryption_process = 0
        self.pushButton_5.clicked.connect(self.return_page)
        self.pushButton_2.clicked.connect(self.select_encrypted_key)
        self.pushButton.clicked.connect(self.choose_modelfiles_direc)
        self.pushButton_4.clicked.connect(self.decrypt_models)
        self.pushButton_3.clicked.connect(self.pick_key_filepath)
        self.pushButton_6.clicked.connect(self.show_decrypt_files)

    def return_page(self):
        self.Choose_Page_Frame = main.ChoosePageFunctionality()
        self.Choose_Page_Frame.show()
        self.close()

    def select_encrypted_key(self):
        keyfile1 = QtWidgets.QFileDialog.getOpenFileName(self)
        self.encryp_key_path = keyfile1[0]

        if self.encryp_key_path != "":
            self.label_2.setText("Encrypted symmetric key successfully chosen")
            print(self.encryp_key_path)
        else:
            self.label_2.setText("You haven't picked a valid keyfile")

    def pick_key_filepath(self):
        keyfile2 = QtWidgets.QFileDialog.getOpenFileName(self)
        self.key_filepath2 = keyfile2[0]
        print(keyfile2[0])

        if self.key_filepath2 != "":
            pk = encryption_func.load_private_key(self.key_filepath2)
            self.pk = pk
            self.label_3.setText("Your selected private key loaded successfully")
        else:
            self.label_3.setText("You haven't picked a valid keyfile")

    def choose_modelfiles_direc(self):
        choosen_direc = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.model_direc = choosen_direc
        direc_list = []

        for id in list(os.walk(self.model_direc))[0][2]:
            direc_list.append(id)

        direc_list = sorted(direc_list, key=str.lower)
        print(direc_list)

        if self.model_direc != "":
            self.label.setText("Choosen directory:" + "\n" + "\n" + self.model_direc)
            print(self.model_direc)

            for name in direc_list:
                self.listWidget.addItem(name)

            self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            self.listWidget.itemClicked.connect(self.on_click_listbox)
        else:
            self.label.setText("You havent picked a valid directory")



    def walk_dir(self, model_direc):
        # walks the specified directory root and returns a list of paths to these files
        file_list = []
        towalk = [model_direc]
        while towalk:
            # TODO not used yet ;)
            root_dir = towalk.pop()
            for path in os.listdir(model_direc):
                full_path = os.path.join(model_direc, path)
                if os.path.isdir(path):
                    continue
                else:
                    # create list of (filename, dir) tuples
                    file_list.append(full_path)

        file_list = sorted(file_list, key=str.lower)
        #print(file_list)
        return file_list

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def on_click_listbox(self):
        file_list = self.walk_dir(self.model_direc)
        if self.listWidget.currentRow() not in self.index:
           self.index.append(self.listWidget.currentRow())
        elif self.listWidget.currentRow() in self.index:
            self.index.remove(self.listWidget.currentRow())

        if len(self.index) == 1:
            self.selpath = [file_list[self.index[0]]]
            path = self.path_leaf(self.selpath[0])
            self.label_5.setText("Selected models:" + "\n" + "\n" + path)
        elif len(self.index) == 0:
            self.label_5.setText("No models selected" + "\n" + "\n" + "Please click on the file(s) to select them")
        else:
            self.selpath = [file_list[x] for x in self.index]
            model_string = "Selected models:"
            for path in self.selpath:
                path = self.path_leaf(path)
                model_string += ("\n" + "\n" + path)

            self.label_5.setText(model_string)



    def decrypt_models(self):

        selected_models = self.selpath

        if self.pk is "":
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Missing Private Key")
            error_dialog.showMessage("There was no RSA private key selected to decrypt the models. Please select and load one.")
            error_dialog.exec_()
        else:
            with open("./functionality/encr_sym_key", "rb") as encr_sym_key:
                encr_key = encr_sym_key.read()
            sym_key = encryption_func.decrypt_symmetric_key(encr_key, self.pk)
            decrypted_models = encryption_func.decrypt_models(selected_models, sym_key)

            for i in range(len(selected_models)):
                with open(selected_models[i], "rb") as decr_model:
                    decr_model.write(decrypted_models[i])

            self.decryption_process = 1

    def show_decrypt_files(self):
        if self.decryption_process == 1:
            os.system('nautilus "/home/felix/PycharmProjects/train-user-client/backend"')
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("No Decryption")
            error_dialog.showMessage("You havent decrypted any modelfiles yet, please select some in your chosen directory and decrypt them")
            error_dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    nextGui = ModelPageFunctionality()
    nextGui.show()
    sys.exit(app.exec_())