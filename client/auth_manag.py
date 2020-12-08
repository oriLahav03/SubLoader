from Windows import *

class Auth_mng():
    def __init__(self, main_mng):
          self.main_mng = main_mng

    def set_ui(self, main_mng):
        self.wig = QtWidgets.QWidget()
        self.win = Ui_LoginForm()
        self.win.setupUi(self.wig, main_mng)
        self.wig.show()
        self.wintype = "login"

    def switch_windows(self):
        self.wig.close() #clean
        self.wig = QtWidgets.QWidget() #new
        if self.wintype == "login":
            self.win = Ui_SingupForm()
            self.win.setupUi(self.wig, self.main_mng)
            self.wig.show()
            self.wintype = "singup"
        else:
            self.win = Ui_LoginForm()
            self.win.setupUi(self.wig, self.main_mng)
            self.wig.show()
            self.wintype = "login"