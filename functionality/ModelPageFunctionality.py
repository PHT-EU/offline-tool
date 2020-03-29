from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from collections import OrderedDict
from visualisation.ModelPage import Ui_MainWindow
from pathlib import Path
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
        self.pk1 = None
        self.direc_list = []
        self.file_list = []
        self.selpath = []
        self.index = []
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
            self.label_2.setText("Encrypted symmetric key successfully chosen")
            print(self.encryp_key_path)
        else:
            self.label_2.setText("You haven't picked a valid keyfile")


    def pick_key_filepath2(self):
        keyfile2 = QtWidgets.QFileDialog.getOpenFileName(self)
        self.key_filepath2 = keyfile2[0]
        pk1 = encryption_func.load_private_key(self.key_filepath2)

        if pk1 == "unvalid":
            self.label_3.setText("You havent picked a valid keyfile")
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Unvalid private key")
            error_dialog.showMessage(
                "The private key you selected wasn´t valid. Choose a valid key or generate a new one")
            error_dialog.exec_()
        else:
            self.pk1 = pk1
            self.label_3.setText(
                "Choosen private key got succesfully loaded and ready to use:" + "\n" + "\n" + self.key_filepath2)



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
        self.label_5.setText("No models selected" + "\n" + "\n" + "Please click on the file(s) to select them")
        del self.index[:]

        for id in list(self.walklevel(self.model_direc, 1))[0][2]:
            self.direc_list.append(id)

        self.direc_list = sorted(self.direc_list, key=str.lower)
        print("directory list", self.direc_list)

        if self.model_direc != "":
            self.label.setText("Choosen directory:" + "\n" + "\n" + self.model_direc)
            print("model direc list", self.model_direc)

            for name in self.direc_list:
                self.listWidget.addItem(name)

            #self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
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

        '''if len(self.index) == 1:
            self.selpath = [self.file_list[self.index[0]]]
            print(self.selpath)
            path = self.path_leaf(self.selpath[0])
            self.label_5.setText("Selected models:" + "\n" + "\n" + path)'''
        if len(self.index) == 0:
            self.label_5.setText("No models selected" + "\n" + "\n" + "Please click on the file(s) to select/deselect them")
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
            error_dialog.showMessage("There was no RSA private key selected to decrypt the models. Please select and load one.")
            error_dialog.exec_()
        else:
            with open(self.encryp_key_path, "rb") as encr_sym_key:
                print("sym key opened")
                encr_key = encr_sym_key.read()
                print("sym key read")
            sym_key = encryption_func.decrypt_symmetric_key(encr_key, self.pk1)
            print("sym key decrypt")
            decrypted_models = encryption_func.decrypt_models(selected_models, sym_key)
            print("models decrypt")

            for i in range(len(selected_models)):
                with open(selected_models[i], "rb") as decr_model:
                    decr_model.write(decrypted_models[i])
            print("model written")
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