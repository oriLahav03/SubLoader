from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Create_Room_Dialog(object):
    def setupUi(self):
        self.Create_Room_Dialog = QtWidgets.QDialog()
        self.Create_Room_Dialog.setObjectName("Create_Room_Dialog")
        self.Create_Room_Dialog.resize(400, 255)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Create_Room_Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.create_btn = QtWidgets.QPushButton(self.Create_Room_Dialog)
        self.create_btn.setObjectName("create_btn")
        self.gridLayout_2.addWidget(self.create_btn, 2, 0, 1, 1)
        self.title_label = QtWidgets.QLabel(self.Create_Room_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAutoFillBackground(False)
        self.title_label.setTextFormat(QtCore.Qt.PlainText)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.gridLayout_2.addWidget(self.title_label, 0, 0, 1, 2)
        self.cancel_btn = QtWidgets.QPushButton(self.Create_Room_Dialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.gridLayout_2.addWidget(self.cancel_btn, 2, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.room_name_label = QtWidgets.QLabel(self.Create_Room_Dialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.room_name_label.setFont(font)
        self.room_name_label.setObjectName("room_name_label")
        self.gridLayout.addWidget(self.room_name_label, 0, 0, 1, 1)
        self.room_name = QtWidgets.QLineEdit(self.Create_Room_Dialog)
        self.room_name.setObjectName("room_name")
        self.gridLayout.addWidget(self.room_name, 0, 1, 1, 1)
        self.room_pass_label = QtWidgets.QLabel(self.Create_Room_Dialog)
        self.room_pass_label.setObjectName("room_pass_label")
        self.gridLayout.addWidget(self.room_pass_label, 1, 0, 1, 1)
        self.room_password = QtWidgets.QLineEdit(self.Create_Room_Dialog)
        self.room_password.setObjectName("room_password")
        self.gridLayout.addWidget(self.room_password, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 2)

        self.retranslateUi(self.Create_Room_Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Create_Room_Dialog)

        self.cancel_btn.clicked.connect(self.cancel_clicked)
        self.create_btn.clicked.connect(self.create_clicked)

        self.Create_Room_Dialog.exec_()

        return self.room_name.text(), self.room_password.text()

    def retranslateUi(self, Create_Room_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Create_Room_Dialog.setWindowTitle(_translate("Create_Room_Dialog", "Create new room"))
        self.create_btn.setText(_translate("Create_Room_Dialog", "Create"))
        self.title_label.setText(_translate("Create_Room_Dialog", "Create new room"))
        self.cancel_btn.setText(_translate("Create_Room_Dialog", "Cancel"))
        self.room_name_label.setText(_translate("Create_Room_Dialog", "Enter the room name here:"))
        self.room_name.setPlaceholderText(_translate("Create_Room_Dialog", "Example: room1"))
        self.room_pass_label.setText(_translate("Create_Room_Dialog", "Enter the room password here: "))
        self.room_password.setPlaceholderText(_translate("Create_Room_Dialog", "Example: password"))

    def cancel_clicked(self):
        self.Create_Room_Dialog.close()

    def create_clicked(self):
        if (self.room_name.text() != "" and self.room_password.text() != "") or not self.cancel_btn.clicked:
            self.Create_Room_Dialog.close()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("You need to enter room name and \nroom password to create the room")
            msgBox.setWindowTitle("Wrong Parameters")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()

