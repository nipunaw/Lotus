# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
import sys
import os
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

DIRECTORY_FILE = "../data/directories.txt"

class UIPreviousWindow(QWidget):
    def __init__(self, parent=None):
        super(UIPreviousWindow, self).__init__(parent)
        # Creates file if not created
        f = open("../data/directories.txt", "w")
        f.close()
        ############ Lotus Logo ###########
        self.logo = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap('assets/lotusSmall.png')
        self.logo.setPixmap(self.pixmap)
        self.logo.show()
        self.create_buttons()


    def create_buttons(self):
        f = open("../data/directories.txt")
        self.directories = f.readlines()
        f.close()
        self.buttons = {}
        for i in range(len(self.directories)):
            self.buttons[self.directories[i]] = QPushButton(self.directories[i], self)
            self.buttons[self.directories[i]].move(63, i * 32 + 32)

