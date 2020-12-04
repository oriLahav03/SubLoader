import sys
import re
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
# from PyQt5 import QtCore as qtc

from Windows import Ui_LoginForm

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    LoginForm = qtw.QWidget()
    ui = Ui_LoginForm()
    ui.setupUi(LoginForm)
    LoginForm.show()

    sys.exit(app.exec_())


