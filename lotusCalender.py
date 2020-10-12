from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class UICalendarWindow(QWidget):
    def __init__(self, parent=None):
        super(UICalendarWindow, self).__init__(parent)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.home_button = QtWidgets.QPushButton("Hub", self.centralwidget)
        self.home_button.setGeometry(QtCore.QRect(10, 10, 60, 60))
        self.home_button.setObjectName("pushButton")

        self.label = QtWidgets.QLabel("Lotus", self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 20, 100, 30))
        self.label.setObjectName("label")

        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 90, 250, 360))
        self.tableView.setObjectName("tableView")

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(280, 90, 480, 460))
        self.calendarWidget.setObjectName("calendarWidget")

        self.help_button = QtWidgets.QPushButton("Help", self.centralwidget)
        self.help_button.setGeometry(QtCore.QRect(580, 30, 80, 25))
        self.help_button.setObjectName("pushButton_2")

        self.settings_button = QtWidgets.QPushButton("Settings", self.centralwidget)
        self.settings_button.setGeometry(QtCore.QRect(690, 30, 80, 25))
        self.settings_button.setObjectName("pushButton_3")

        self.schedule_notes_button = QtWidgets.QPushButton("Add New Scheduled Notes", self.centralwidget)
        self.schedule_notes_button.setGeometry(QtCore.QRect(20, 480, 240, 50))
        self.schedule_notes_button.setObjectName("pushButton_4")

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")