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


class CircleButton(QtWidgets.QPushButton):
    def __init__(self, directory, directory_darker, parent=None):
        super(CircleButton, self).__init__(parent)
        self.setFixedSize(120, 120)
        #self.setIcon(QtGui.QIcon(directory))
        #self.setIconSize(self.size())
        #self.setMouseTracking(True)
        self.setMask(QtGui.QRegion(QtCore.QRect(-1, -1, 122, 122), QtGui.QRegion.Ellipse))
        self.setStyleSheet("CircleButton {border-image: url("+directory+");} CircleButton:hover {border-image: url("+directory_darker+");}")