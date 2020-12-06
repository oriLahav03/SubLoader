import sys
import re
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from client_logic import *
# from PyQt5 import QtCore as qtc

from auth_manag import *

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    auth_mng = Auth_mng()

    sys.exit(app.exec_())


