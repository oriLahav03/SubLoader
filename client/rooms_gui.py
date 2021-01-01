from room_gui import Ui_room
from SettingsDialog.Create_room_dialog import *
from SettingsDialog.Join_room_dialog import *


ROOMS = {
       'room1': {
           'members': ['ori', 'ilay', 'yossi1'],
           'password': "123"
       },
       'room2': {
           'members': ['ori', 'ilay', 'yossi2'],
           'password': "456"
       },
       'room3': {
           'members': ['ori', 'ilay', 'yossi3'],
           'password': "789"
       },
       'room4': {
           'members': ['ori', 'ilay', 'yossi1'],
           'password': "101"
       },
       'room5': {
           'members': ['ori', 'ilay', 'yossi2'],
           'password': "112"
       },
       'room6': {
           'members': ['ori', 'ilay', 'yossi3'],
           'password': "131"
       }
}
USER_NAME = "Ori"


class Ui_MainWindow(object):

    def setupUi(self, MainWindow, rooms, user_ip):
        """
        the function setup all the application content
        :param MainWindow: the main window
        :param rooms: the rooms of the user
        :param user_ip: the ip of the user
        :return: None
        """
        # Main window setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(425, 500)

        # QtWidgets Setups
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.IP_label = QtWidgets.QLabel(self.central_widget)
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.rooms = rooms
        self.menu_Room = QtWidgets.QMenu(self.menu_bar)
        self.menu_Room.setObjectName("menuRoom")
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.actionCreate_room = QtWidgets.QAction(MainWindow)
        self.actionCreate_room.setObjectName("actionCreate_room")
        self.actionJoin_room = QtWidgets.QAction(MainWindow)
        self.actionJoin_room.setObjectName("actionJoin_room")
        self.actionCreate_room.triggered.connect(self.open_create_room_dialog)  # new dialog
        self.actionJoin_room.triggered.connect(self.open_join_room_dialog)  # new dialog
        self.actionCreate_room_2 = QtWidgets.QAction(MainWindow)
        self.actionCreate_room_2.setObjectName("actionCreate_room_2")
        self.menu_Room.addAction(self.actionCreate_room)
        self.menu_Room.addAction(self.actionJoin_room)
        self.menu_bar.addAction(self.menu_Room.menuAction())
        self.verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                    QtWidgets.QSizePolicy.Expanding)

        # Set up MainWindow - continue
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.central_widget)

        # What is my ip label setup
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.IP_label.setFont(font)
        self.IP_label.setAlignment(QtCore.Qt.AlignCenter)
        self.IP_label.setObjectName("IP_label")
        self.verticalLayout.addWidget(self.IP_label)

        # Scroll setup
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 330, 599))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # MenuBar setup
        MainWindow.setCentralWidget(self.central_widget)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 354, 26))
        self.menu_bar.setObjectName("menu_bar")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        # Adding the Widgets of the rooms
        self.update_rooms()

        # Set names
        self.retranslateUi(MainWindow, user_ip)

        # Run
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, mainWindow, user_ip):
        """
        The function set all the names.
        :param user_ip: the ip of the user
        :param mainWindow: the main window
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "SubLoader"))
        self.IP_label.setText(_translate("MainWindow", "your ip is: " + user_ip))
        self.menu_Room.setTitle(_translate("MainWindow", "Room"))
        self.actionCreate_room.setText(_translate("MainWindow", "Create room"))
        self.actionJoin_room.setText(_translate("MainWindow", "Join room"))
        self.actionCreate_room_2.setText(_translate("MainWindow", "Create room"))

    def open_create_room_dialog(self):
        window = Ui_Create_Room_Dialog()
        room_name, room_pass, cancel = window.setupUi()
        if room_name != '' and room_pass != '' and not cancel:
            ROOMS[room_name] = dict()  # TODO: add to rooms list
            ROOMS[room_name]['members'] = list()
            ROOMS[room_name]['password'] = room_pass
            for key, value in ROOMS.items():
                print(f'{key} {str(value)}')

    def open_join_room_dialog(self):
        window = Ui_Join_Room_Dialog()
        room_name, room_pass, cancel = window.setupUi()
        if cancel:
            pass
        elif room_name in ROOMS.keys() and room_pass == ROOMS[room_name]['password']:
            ROOMS[room_name]['members'].append(USER_NAME)  # TODO: get list from db
            for key, value in ROOMS.items():
                print(f'{key} {str(value)}')
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("Invalid room name or password")
            msgBox.setWindowTitle("Wrong Parameters")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()

    def update_rooms(self):
        for room_name, members in self.rooms.items():
            room = Ui_room()
            _room = {Ui_room.setObjectName(room, room_name), Ui_room.setFixedWidth(room, 350),
                     Ui_room.setWindowTitle(room, "room")}
            Ui_room.setupUi(room, _room=_room, members=members['members'], _room_name=room_name)
            room.adjustSize()
            self.verticalLayout_2.addWidget(room)
            self.verticalLayout_2.addSpacerItem(self.verticalSpacer)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    _MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(_MainWindow, ROOMS, '25.200.0.10')
    _MainWindow.show()
    sys.exit(app.exec_())

