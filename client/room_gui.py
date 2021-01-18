from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_room(QtWidgets.QWidget):
    def __init__(self):
        """
        initialize the code
        """
        super(Ui_room, self).__init__()
        self.installEventFilter(self)
        self.buttons = list()
        self.members = list()
        self.holder = QtWidgets.QVBoxLayout()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)

    def eventFilter(self, QObject, event):
        """
        catch all the events of the application
        :param QObject: the object
        :param event: the event
        :return: None
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                print("Right button clicked")
        return False

    def setupUi(self, _room, members: list, _room_name: str):
        """
        the function setup all the application content
        :param _room: the room
        :param members: the members in the room
        :param _room_name: the name of the room
        :return: None
        """

        # Creating the layout of the widget
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.holder.setObjectName("holder")
        self.verticalLayout_2.addLayout(self.holder)

        # Creating the room
        self.set__room(_room_name)

        # Add the members to the room
        for member in members:
            self.set_member(member)

        # Show and hide the members of room when button pressed
        for button in self.buttons:
            button.clicked.connect(self.change_visibility)

        # Set the names
        self.retranslateUi(self)

        # Run
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, _room):
        """
        set names
        :param _room: the room name
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate

    def set__room(self, _room_name):
        """
        creating the rooms
        :param _room_name: the name of the room
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        temp = QtWidgets.QPushButton(self)
        temp.setObjectName(_room_name)
        temp.setText(_translate('room', _room_name))
        temp.setMinimumSize(200, 30)
        self.holder.addWidget(temp)
        self.buttons.append(temp)

    def set_member(self, member):
        """
        Put the members of a room in it
        :param member: the member
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        temp = QtWidgets.QPushButton(self)
        temp.setObjectName(member)
        temp.setText(_translate('room', member))
        temp.setStyleSheet("background: transparent;")
        temp.setMinimumSize(200, 30)
        self.holder.addWidget(temp)
        self.members.append(temp)

    def change_visibility(self):
        """
        the function hide and show the members of the room clicked
        :return: None
        """
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
