from PyQt5 import QtCore, QtGui, QtWidgets
#from fbs_runtime.application_context.PyQt5 import ApplicationContext
from visualisation.ChoosePage import Ui_MainWindow
from functionality import ModelPageFunctionality
from functionality.SecurityValuesFunctionality import SecurityValuesFunctionality
import sys


class ChoosePageFunctionality(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(ChoosePageFunctionality, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.switch_to_security)
        self.pushButton_2.clicked.connect(self.switch_to_model)
        self.label5_text = "Copyright" + " © " + "<a href=\"https://pht.difuture.de\"><font color=black> MIT </font></a>" + "created 2020, by Felix.B"
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

    @staticmethod
    def link_handler():
        text = "MIT License" + "\n" + "\n" + "Copyright (c) 2020 Personal Health Train / Implementations / GermanMII / DIFUTURE / Train Image" + "\n" +"\n" + "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:" + "\n" + "\n" + "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." + "\n" + "\n" + "THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Copyright")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    nextGui = ChoosePageFunctionality()
    nextGui.show()
    sys.exit(app.exec_())