 # CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
import sys
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

class UIPreviousWindow(QWidget):
    def __init__(self, parent=None):
        super(UIPreviousWindow, self).__init__(parent)

        ############ Lotus Logo ###########
        self.logo = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap('assets/lotusSmall.png')
        self.logo.setPixmap(self.pixmap)
        self.logo.show()

        self.create_buttons()

    def create_buttons(self):
        with open('../data/directories.txt', "w+") as f:
            self.directories = f.readlines()

        self.buttons = {}
        for i in range(len(self.directories)):
            self.buttons[self.directories[i]] = QPushButton(self.directories[i], self)
            self.buttons[self.directories[i]].move(63, i * 32 + 32)




