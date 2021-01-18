from room_gui import *
from Create_room_dialog import *
from Join_room_dialog import *


ROOMS = {
       'room1': ['ori', 'ilay', 'yossi1'],
       'room2': ['ori', 'ilay', 'yossi2'],
       'room3': ['ori', 'ilay', 'yossi3'],
       'room4': ['ori', 'ilay', 'yossi1'],
       'room5': ['ori', 'ilay', 'yossi2'],
       'room6': ['ori', 'ilay', 'yossi3']
}
USER_NAME = "Ori"


class Ui_RoomsWindow(object):

    def setupUi(self, MainWindow, rooms, user_ip):
        """
        the function setup all the application content
        :param MainWindow: the main window
        :param rooms: the rooms of the user
        :param user_ip: the ip of the user
        :return: None
        """
        # Main window setup
        self.wig = MainWindow
        self.wig.setObjectName("MainWindow")
        self.wig.setFixedSize(425, 500)

        # QtWidgets Setups
        self.central_widget = QtWidgets.QWidget(self.wig)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.IP_label = QtWidgets.QLabel(self.central_widget)
        self.scrollArea = QtWidgets.QScrollArea(self.central_widget)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.menu_bar = QtWidgets.QMenuBar(self.wig)
        self.rooms = rooms
        self.menu_Room = QtWidgets.QMenu(self.menu_bar)
        self.menu_Room.setObjectName("menuRoom")
        self.status_bar = QtWidgets.QStatusBar(self.wig)
        self.actionCreate_room = QtWidgets.QAction(self.wig)
        self.actionCreate_room.setObjectName("actionCreate_room")
        self.actionJoin_room = QtWidgets.QAction(self.wig)
        self.actionJoin_room.setObjectName("actionJoin_room")
        self.actionCreate_room.triggered.connect(self.open_create_room_dialog)  # new dialog
        self.actionJoin_room.triggered.connect(self.open_join_room_dialog)  # new dialog
        self.actionCreate_room_2 = QtWidgets.QAction(self.wig)
        self.actionCreate_room_2.setObjectName("actionCreate_room_2")
        self.menu_Room.addAction(self.actionCreate_room)
        self.menu_Room.addAction(self.actionJoin_room)
        self.menu_bar.addAction(self.menu_Room.menuAction())
        self.verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                    QtWidgets.QSizePolicy.Expanding)

        # Set up MainWindow - continue
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout.setObjectName("verticalLayout")
        self.wig.setCentralWidget(self.central_widget)

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
        self.wig.setCentralWidget(self.central_widget)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 354, 26))
        self.menu_bar.setObjectName("menu_bar")
        self.wig.setMenuBar(self.menu_bar)
        self.status_bar.setObjectName("status_bar")
        self.wig.setStatusBar(self.status_bar)

        # Adding the Widgets of the rooms
        self.update_rooms()

        # Set names
        self.retranslateUi(self.wig, user_ip)
        # Run
        QtCore.QMetaObject.connectSlotsByName(self.wig)
    
    def retranslateUi(self, mainWindow, user_ip):
        """
        The function set all the names.
        :param user_ip: the ip of the user
        :param mainWindow: the main window
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "SubLoader"))
        self.IP_label.setText(_translate("MainWindow", "user,ip: " + user_ip))
        self.menu_Room.setTitle(_translate("MainWindow", "Room"))
        self.actionCreate_room.setText(_translate("MainWindow", "Create room"))
        self.actionJoin_room.setText(_translate("MainWindow", "Join room"))
        self.actionCreate_room_2.setText(_translate("MainWindow", "Create room"))

    def open_create_room_dialog(self):
        """make the create room dialog page
            and show it
        """
        window = Ui_Create_Room_Dialog()
        room_name, room_pass, cancel = window.setupUi()
        if room_name != '' and not cancel:
            ROOMS[room_name] = list()  # TODO: add to rooms list
            for key, value in ROOMS.items():
                print(f'{key} {str(value)}')

    def open_join_room_dialog(self):
        """make the join room dialog page
            and show it
        """
        window = Ui_Join_Room_Dialog()
        room_name, room_pass, cancel = window.setupUi()
        if cancel:
            pass
        elif room_name in ROOMS.keys():
            ROOMS[room_name].append(USER_NAME)  # TODO: get username and append to db room members list
            for key, value in ROOMS.items():
                print(f'{key} {str(value)}')
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("Invalid room name or password")
            msgBox.setWindowTitle("Wrong Parameters")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec()

    def __build_rooms_data(self, rooms_data):
        """convert the data from the logic that came in dict 
        but the value is a list and not olny str for ip

        Args:
            rooms_data (dict): [data from the logic]

        Returns:
            [dict]: [data that the gui can display]
        """
        temp_data = {}
        for n,dt in rooms_data.items():
            temp_data[n] = dt[0]
        return temp_data

    def update_rooms(self):
        """update the rooms view if a room added or delted
        use only after update the room list data
        """

        for room_name, members in self.rooms.items():
            room = Ui_room()
            _room = {Ui_room.setObjectName(room, room_name), Ui_room.setFixedWidth(room, 350),
                     Ui_room.setWindowTitle(room, "room")}
            Ui_room.setupUi(room, _room=_room, members=members, _room_name=room_name)
            room.adjustSize()
            self.verticalLayout_2.addWidget(room)
            self.verticalLayout_2.addSpacerItem(self.verticalSpacer)

    def add_room(self, room_name, members):
        """add single room to the app view

        Args:
            room_name (str): [the name of the room]
            members (list): [list of user's ip that in the room]
        """
        room = Ui_room()
        _room = {Ui_room.setObjectName(room, room_name), Ui_room.setFixedWidth(room, 350),
                    Ui_room.setWindowTitle(room, "room")}
        Ui_room.setupUi(room, _room=_room, members=members, _room_name=room_name)
        room.adjustSize()
        self.verticalLayout_2.addWidget(room)
        self.verticalLayout_2.addSpacerItem(self.verticalSpacer)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    _MainWindow = QtWidgets.QMainWindow()
    ui = Ui_RoomsWindow()
    ui.setupUi(_MainWindow, ROOMS, '25.200.0.10')
    _MainWindow.show()
    sys.exit(app.exec_())

