import sys
from PyQt5 import QtWidgets as qtw
from auth_manag import *


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    auth_mng = Auth_mng()

    sys.exit(app.exec_())
