from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_room(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_room, self).__init__()
        self.installEventFilter(self)
        self.buttons = list()
        self.members = list()
        self.holder = QtWidgets.QVBoxLayout()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)

    def eventFilter(self, QObject, event):
        print("hahha")
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                print("Right button clicked")
        return False

    def setupUi(self, _room, members: list, _room_name: str):
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.holder.setObjectName("holder")
        self.verticalLayout_2.addLayout(self.holder)

        self.set__room(_room_name)

        for member in members:
            self.set_member(member)

        for button in self.buttons:
            button.clicked.connect(self.change_visibility)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, _room):
        _translate = QtCore.QCoreApplication.translate

    def set__room(self, _room_name):
        _translate = QtCore.QCoreApplication.translate
        temp = QtWidgets.QPushButton(self)
        temp.setObjectName(_room_name)
        temp.setText(_translate('room', _room_name))
        temp.setMinimumWidth(300)
        self.holder.addWidget(temp)
        self.buttons.append(temp)

    def set_member(self, member):
        _translate = QtCore.QCoreApplication.translate
        temp = QtWidgets.QPushButton(self)
        temp.setObjectName(member)
        temp.setText(_translate('room', member))
        temp.setStyleSheet("background: transparent;")
        self.holder.addWidget(temp)
        self.members.append(temp)

    def change_visibility(self):
        for member in self.members:
            if member.isVisible():
                member.setVisible(False)
            else:
                member.setVisible(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    _room = QtWidgets.QWidget()
    ui = Ui_room()
    ui.setupUi(_room, ['25.0.0.2 - ori', '25.0.0.3 - ilay', '25.0.0.4 - michael'], 'Me&&TheBoys')
    _room.show()
    sys.exit(app.exec_())
