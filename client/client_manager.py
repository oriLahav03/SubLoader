from client_logic import *
from auth_manag import *
import sys
import re
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

class Manager():
    def __init__(self):
        self.logic = Client_logic()
        self.auth_mng = Auth_mng(self)
        self.gui_app = qtw.QApplication(sys.argv)
        self.start_gui()

    def make_singup(self):
        try:
            args = self.auth_mng.win.get_labels()
            res = self.logic.do_singup(args[0], args[1], args[2], args[3])
            if res:
                qtw.QMessageBox.critical(self.auth_mng.wig, 'Fail', str(res))
            else:
                self.next_win()
        except (email_err, pw_err, un_err) as e:
            qtw.QMessageBox.critical(self.auth_mng.wig, 'INPUT ERROR', str(e))

        
    def make_login(self):
        try:
            args = self.auth_mng.win.get_labels()
            res = self.logic.do_login(args[0], args[1])
            if res:
                qtw.QMessageBox.critical(self.auth_mng.wig, 'Fail', 'login unsuccessful \nusername or password incorrect')
            else:
                self.next_win()
        except (email_err, pw_err) as e:
            qtw.QMessageBox.critical(self.auth_mng.wig, 'INPUT ERROR', str(e))

    def next_win(self, win = None):
        print("*room window*")
     
    def start_gui(self):
        self.auth_mng.set_ui(self)
        sys.exit(self.gui_app.exec_())

if __name__ == '__main__':
    mang = Manager()
    