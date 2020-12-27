from room_gui import Ui_room


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
        self.menu_settings = QtWidgets.QMenu(self.menu_bar)
        self.menu_info = QtWidgets.QMenu(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
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
        self.menu_settings.setObjectName("menu_settings")
        self.menu_info.setObjectName("menu_info")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.menu_bar.addAction(self.menu_settings.menuAction())
        self.menu_bar.addAction(self.menu_info.menuAction())

        # Adding the Widgets of the rooms
        for room_name, members in rooms.items():
            room = Ui_room()
            _room = {Ui_room.setObjectName(room, room_name), Ui_room.setFixedWidth(room, 350),
                     Ui_room.setWindowTitle(room, "room")}
            Ui_room.setupUi(room, _room=_room, members=members, _room_name=room_name)
            room.adjustSize()
            self.verticalLayout_2.addWidget(room)
            self.verticalLayout_2.addSpacerItem(self.verticalSpacer)

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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    _MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(_MainWindow,
               {
                   'room1': ['ori', 'ilay', 'yossi1'],
                   'room2': ['ori', 'ilay', 'yossi2'],
                   'room3': ['ori', 'ilay', 'yossi3'],
                   'room4': ['ori', 'ilay', 'yossi1'],
                   'room5': ['ori', 'ilay', 'yossi2'],
                   'room6': ['ori', 'ilay', 'yossi3']
               }, '25.200.0.10')
    _MainWindow.show()
    sys.exit(app.exec_())
