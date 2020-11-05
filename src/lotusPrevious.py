# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.uic.properties import QtCore

from src.constants import DIRECTORY_FILE

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
        self.create_buttons()

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
