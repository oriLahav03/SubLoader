import re
from PyQt5 import QtCore, QtGui, QtWidgets

# Email must be in a some@some.com format
email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

# Password must contain:
# At list 1 Uppercase letter
# At list 1 number
# At list 6 chars
password_regex = r'[A-Za-z0-9]{6,}'


def login_screen():
    LoginForm = QtWidgets.QWidget()
    ui = Ui_LoginForm()
    ui.setupUi(LoginForm)
    LoginForm.show()


class Ui_LoginForm(QtWidgets.QWidget):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(398, 200)

        # Title
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title = QtWidgets.QLabel(LoginForm)
        self.title.setGeometry(QtCore.QRect(0, 0, 401, 51))
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")

        # Email Label
        self.email_label = QtWidgets.QLabel(LoginForm)
        self.email_label.setGeometry(QtCore.QRect(10, 50, 101, 41))
        self.email_label.setObjectName("email_label")

        # Email Input
        self.email_text = QtWidgets.QLineEdit(LoginForm)
        self.email_text.setGeometry(QtCore.QRect(80, 60, 301, 22))
        self.email_text.setObjectName("email_text")

        # Password Label
        self.password_label = QtWidgets.QLabel(LoginForm)
        self.password_label.setGeometry(QtCore.QRect(10, 90, 101, 41))
        self.password_label.setObjectName("password_label")

        # Password Input
        self.password_text = QtWidgets.QLineEdit(LoginForm)
        self.password_text.setGeometry(QtCore.QRect(80, 100, 301, 22))
        self.password_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_text.setObjectName("password_text")

        # Login Press Button
        font = QtGui.QFont()
        font.setPointSize(14)
        self.login_button = QtWidgets.QPushButton(LoginForm)
        self.login_button.setGeometry(QtCore.QRect(190, 140, 211, 71))
        self.login_button.setFont(font)
        self.login_button.setObjectName("login_button")

        # Go Back To Signup Button
        font.setPointSize(14)
        self.back_to_singup = QtWidgets.QPushButton(LoginForm)
        self.back_to_singup.setGeometry(QtCore.QRect(-8, 140, 201, 71))
        self.back_to_singup.setFont(font)
        self.back_to_singup.setObjectName("back_to_singup")

        # Raises
        self.password_label.raise_()
        self.password_text.raise_()
        self.email_text.raise_()
        self.login_button.raise_()
        self.title.raise_()
        self.email_label.raise_()
        self.back_to_singup.raise_()

        self.retranslateUi(LoginForm)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

        self.login_button.clicked.connect(self.authenticate)

        self.back_to_singup.clicked.connect(self.signup_screen)

    def signup_screen(self):
        self.SignupForm = QtWidgets.QWidget()
        self.ui = Ui_SingupForm()
        self.ui.setupUi(self.SignupForm)
        self.SignupForm.show()

    def check_mail(self):
        if re.search(email_regex, self.email_text.text()):
            return True
        else:
            return False

    def check_password(self):
        if re.fullmatch(password_regex, self.password_text.text()):
            return True
        else:
            return False

    def authenticate(self):
        # email = self.email_text.text()
        # password = self.password_text.text()

        if self.check_mail() and self.check_password():
            QtWidgets.QMessageBox.information(self, 'Success', 'Login successful!')
        else:
            QtWidgets.QMessageBox.critical(self, 'Fail', 'Login failed')

    def retranslateUi(self, LoginForm):
        """
        the function set up the texts
        :param LoginForm: the LoginForm
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "SubLoader"))
        self.title.setText(_translate("LoginForm", "Login to Subloader"))
        self.email_label.setText(_translate("LoginForm", "email:"))
        self.password_label.setText(_translate("LoginForm", "Password:"))
        self.login_button.setText(_translate("LoginForm", "Login"))
        self.back_to_singup.setText(_translate("LoginForm", "Go to Singup"))


class Ui_SingupForm(object):
    def setupUi(self, SingupForm):
        SingupForm.setObjectName("SingupForm")
        SingupForm.resize(477, 344)
        
        # Singup Label
        font = QtGui.QFont()
        font.setPointSize(16)
        self.signup_label = QtWidgets.QLabel(SingupForm)
        self.signup_label.setGeometry(QtCore.QRect(110, -10, 301, 81))
        self.signup_label.setFont(font)
        self.signup_label.setObjectName("signup_label")

        # Password Input
        self.password_text = QtWidgets.QLineEdit(SingupForm)
        self.password_text.setGeometry(QtCore.QRect(130, 150, 301, 22))
        self.password_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_text.setObjectName("password_text")

        # Password Label
        self.password_label = QtWidgets.QLabel(SingupForm)
        self.password_label.setGeometry(QtCore.QRect(10, 140, 101, 41))
        self.password_label.setObjectName("password_label")

        # Username Input
        self.username_text = QtWidgets.QLineEdit(SingupForm)
        self.username_text.setGeometry(QtCore.QRect(130, 110, 301, 22))
        self.username_text.setObjectName("username_text")

        # Username Label
        self.username_label = QtWidgets.QLabel(SingupForm)
        self.username_label.setGeometry(QtCore.QRect(10, 100, 101, 41))
        self.username_label.setObjectName("username_label")

        # Email Label
        self.email_label = QtWidgets.QLabel(SingupForm)
        self.email_label.setGeometry(QtCore.QRect(10, 60, 101, 41))
        self.email_label.setObjectName("email_label")

        # Email Input
        self.email_text = QtWidgets.QLineEdit(SingupForm)
        self.email_text.setGeometry(QtCore.QRect(130, 70, 301, 22))
        self.email_text.setObjectName("email_text")

        # Confirm Password Input
        self.confirm_password_text = QtWidgets.QLineEdit(SingupForm)
        self.confirm_password_text.setGeometry(QtCore.QRect(130, 190, 301, 22))
        self.confirm_password_text.setText("")
        self.confirm_password_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_text.setObjectName("confirm_password_text")

        # Confirm Password Label
        self.confirm_password_label = QtWidgets.QLabel(SingupForm)
        self.confirm_password_label.setGeometry(QtCore.QRect(10, 180, 111, 41))
        self.confirm_password_label.setObjectName("confirm_password_label")

        # Agree To Terms Checkbox
        font = QtGui.QFont()
        font.setPointSize(6)
        self.agree_to_terms_checkbox = QtWidgets.QCheckBox(SingupForm)
        self.agree_to_terms_checkbox.setGeometry(QtCore.QRect(10, 230, 461, 21))
        self.agree_to_terms_checkbox.setFont(font)
        self.agree_to_terms_checkbox.setAutoFillBackground(False)
        self.agree_to_terms_checkbox.setObjectName("agree_to_terms_checkbox")

        # Create The Account Button
        font = QtGui.QFont()
        font.setPointSize(14)
        self.create_account_button = QtWidgets.QPushButton(SingupForm)
        self.create_account_button.setGeometry(QtCore.QRect(230, 270, 251, 81))
        self.create_account_button.setFont(font)
        self.create_account_button.setObjectName("create_account_button")

        # Go Back To Login Screen Button
        font = QtGui.QFont()
        font.setPointSize(12)
        self.back_to_login_button = QtWidgets.QPushButton(SingupForm)
        self.back_to_login_button.setGeometry(QtCore.QRect(-10, 270, 241, 81))
        self.back_to_login_button.setFont(font)
        self.back_to_login_button.setObjectName("back_to_login_button")

        self.retranslateUi(SingupForm)
        QtCore.QMetaObject.connectSlotsByName(SingupForm)

        self.back_to_login_button.clicked.connect(self.signup_screen)
        # self.back_to_login_button.clicked.connect(self.hide_window)

    # def hide_window(self, Signup):
    #     Signup.hide()

    def signup_screen(self):
        self.LoginForm = QtWidgets.QWidget()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self.LoginForm)
        self.LoginForm.show()

    def retranslateUi(self, SingupForm):
        _translate = QtCore.QCoreApplication.translate
        SingupForm.setWindowTitle(_translate("SingupForm", "Signup"))
        self.signup_label.setText(_translate("SingupForm", "Singup to Subloader"))
        self.password_label.setText(_translate("SingupForm", "Password:"))
        self.username_label.setText(_translate("SingupForm", "Username:"))
        self.email_label.setText(_translate("SingupForm", "Email"))
        self.confirm_password_label.setText(_translate("SingupForm", "Confirm Password:"))
        self.agree_to_terms_checkbox.setText(_translate("SingupForm",
                                                        "By creating an account, you agree to the Terms of Service "
                                                        "and acknowledge our Privacy Policy."))
        self.create_account_button.setText(_translate("SingupForm", "Create"))
        self.back_to_login_button.setText(_translate("SingupForm", "Go back to Login screen"))


