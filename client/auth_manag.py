from Windows import *


class Auth_mng:
    def __init__(self, main_mng):
        self.wintype = "login"
        self.main_mng = main_mng

    def set_ui(self, main_mng):
        """
        The function setup the new window
        :param main_mng: The main manager window
        :return: None
        """
        self.wig = QtWidgets.QWidget()
        self.win = Ui_LoginForm()
        self.win.setupUi(self.wig, main_mng)
        self.wig.show()
        self.wintype = "login"

    def switch_windows(self):
        """
        The function switch between login window and signup window
        :return: None
        """
        self.wig.close()  # clean
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

