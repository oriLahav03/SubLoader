from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Join_Room_Dialog(object):
    def __init__(self):
        self.cancel = True

    def setupUi(self):
        """
        The function handle the user join room event
        :return: None
        """
        self.Join_Room_Dialog = QtWidgets.QDialog()
        self.Join_Room_Dialog.setObjectName("Join_Room_Dialog")
        self.Join_Room_Dialog.resize(400, 255)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Join_Room_Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.title_label = QtWidgets.QLabel(self.Join_Room_Dialog)
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.room_pass_label = QtWidgets.QLabel(self.Join_Room_Dialog)
        self.room_pass_label.setObjectName("room_pass_label")
        self.gridLayout.addWidget(self.room_pass_label, 1, 0, 1, 1)
        self.room_password = QtWidgets.QLineEdit(self.Join_Room_Dialog)
        self.room_password.setObjectName("room_password")
        self.gridLayout.addWidget(self.room_password, 1, 1, 1, 1)
        self.room_name = QtWidgets.QLineEdit(self.Join_Room_Dialog)
        self.room_name.setObjectName("room_name")
        self.gridLayout.addWidget(self.room_name, 0, 1, 1, 1)
        self.room_name_label = QtWidgets.QLabel(self.Join_Room_Dialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.room_name_label.setFont(font)
        self.room_name_label.setObjectName("room_name_label")
        self.gridLayout.addWidget(self.room_name_label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 2)
        self.join_btn = QtWidgets.QPushButton(self.Join_Room_Dialog)
        self.join_btn.setObjectName("join_btn")
        self.gridLayout_2.addWidget(self.join_btn, 2, 0, 1, 1)
        self.cancel_btn = QtWidgets.QPushButton(self.Join_Room_Dialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.gridLayout_2.addWidget(self.cancel_btn, 2, 1, 1, 1)
        self.Join_Room_Dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.cancel = False

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Join_Room_Dialog)

        self.cancel_btn.clicked.connect(self.cancel_clicked)
        self.join_btn.clicked.connect(self.join_clicked)

        self.Join_Room_Dialog.exec_()

        return str(self.room_name.text()), str(self.room_password.text()), self.cancel

    def retranslateUi(self):
        """
        The function set the names for the boxes
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.Join_Room_Dialog.setWindowTitle(_translate("Join_Room_Dialog", "Join room"))
        self.title_label.setText(_translate("Join_Room_Dialog", "Join room"))
        self.room_pass_label.setText(_translate("Join_Room_Dialog", "Enter the room password here: "))
        self.room_password.setPlaceholderText(_translate("Join_Room_Dialog", "Example: password"))
        self.room_name.setPlaceholderText(_translate("Join_Room_Dialog", "Example: room1"))
        self.room_name_label.setText(_translate("Join_Room_Dialog", "Enter the room name here:"))
        self.join_btn.setText(_translate("Join_Room_Dialog", "Join"))
        self.cancel_btn.setText(_translate("Join_Room_Dialog", "Cancel"))

    def cancel_clicked(self):
        """
        The function check if the user clicked the cancel click to cancel the joining
        :return: None
        """
        self.Join_Room_Dialog.close()

    def join_clicked(self):
        """
        The function handle the join button pressed event, when the user join a room
        :return: None
        """
        if self.room_name.text() != "" or not self.cancel_btn.clicked:
            self.Join_Room_Dialog.close()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("You need to enter room name to join the room")
            msgBox.setWindowTitle("Wrong Parameters")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
