# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.uic.properties import QtCore

from src.constants import DIRECTORY_FILE, SCHEDULE_FILE_PATH, assets
import json

class UIPreviousWindow(QWidget):
    def __init__(self, set_paths, parent=None):
        super(UIPreviousWindow, self).__init__(parent)
        self.set_paths = set_paths
        # Creates file if not created
        try:
            file = open(DIRECTORY_FILE, 'r')
        except IOError:
            file = open(DIRECTORY_FILE, 'w')
        file.close()
        ############ Lotus Logo ###########
        #self.logo = QtWidgets.QLabel(self)
        #self.pixmap = QtGui.QPixmap('assets/lotusSmall.png')
        #self.logo.setPixmap(self.pixmap)
        #self.logo.show()
        self.container_ui()
        self.create_buttons()

    def container_ui(self):
        self.setFixedSize(600, 400)
        self.container_layout = QtWidgets.QGridLayout()

        try:
            with open(SCHEDULE_FILE_PATH) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        name_classes = []
        for b in data:
            name_classes.append(b['name'])

        row = 0
        _id = QtGui.QFontDatabase.addApplicationFont(assets["lato"])
        button_style = "QPushButton {background-color: white; border: 1px solid #e1e1e1; text-align: left; font-size: 13px; font-family: Lato} QPushButton::hover {background-color: #e1e1e1;}"
        for i in name_classes:
            class_button = QtWidgets.QPushButton(i)
            class_button.setFixedHeight(30)
            class_button.setStyleSheet(button_style)
            class_button.clicked.connect(self.create_buttons)
            self.container_layout.addWidget(class_button, row, 0)
            row += 1

        recent_button = QtWidgets.QPushButton("Recent Notes")
        recent_button.setFixedHeight(30)
        recent_button.clicked.connect(self.create_buttons)
        recent_button.setStyleSheet(button_style)
        self.container_layout.addWidget(recent_button, row, 0)

        vertical_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.container_layout.addItem(vertical_spacer, row+1, 0)

        self.container_layout.setHorizontalSpacing(0)
        self.container_layout.setVerticalSpacing(0)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        #self.container_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)


        self.setLayout(self.container_layout)


    def delete_button(self, str):
        for i in range(0, len(self.directories)):
            b : QPushButton = self.buttons[self.directories[i]]
            if b.text() == str:
                b.hide()

    def create_buttons(self):
        f = open(DIRECTORY_FILE, "r")
        self.directories = f.readlines()
        f.close()

        self.layout = QtWidgets.QGridLayout()

        if len(self.directories) == 0:
            self.no_notes_text = QtWidgets.QLabel()
            self.no_notes_text.setText("No non-scheduled notes to display")
            self.layout.addWidget(self.no_notes_text)
        else:
            self.buttons = {}
            if not self.set_paths:
                for i in range(len(self.directories)):
                    self.buttons[self.directories[i]] = QPushButton(self.directories[i], self)
                    self.buttons[self.directories[i]].setIcon(QIcon(QPixmap(self.directories[i].strip())))
                    self.buttons[self.directories[i]].setIconSize(QSize(100,100))
                    self.layout.addWidget(self.buttons[self.directories[i]], i, 1)
                self.setLayout(self.layout)

            else:
                for i in range(len(self.directories)):
                    self.buttons[self.directories[i]] = QPushButton(self.directories[i], self)
                    self.layout.addWidget(self.buttons[self.directories[i]], i, 1)
                self.setLayout(self.layout)
