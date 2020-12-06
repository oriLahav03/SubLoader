from Windows import *

class Auth_mng():
    def __init__(self):
        self.wig = QtWidgets.QWidget()
        self.win = Ui_LoginForm()
        self.win.setupUi(self.wig, self)
        self.wig.show()
        self.wintype = "login"

    def switch_windows(self):
        self.wig.close() #clean
        self.wig = QtWidgets.QWidget() #new
        if self.wintype == "login":
            self.win = Ui_SingupForm()
            self.win.setupUi(self.wig, self)
            self.wig.show()
            self.wintype = "singup"
        else:
            self.win = Ui_LoginForm()
            self.win.setupUi(self.wig, self)
            self.wig.show()
            self.wintype = "login"