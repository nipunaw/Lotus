# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class CircleButton(QtWidgets.QPushButton):
    def __init__(self, directory, directory_darker, x=120, y=120, parent=None):
        super(CircleButton, self).__init__(parent)
        self.setFixedSize(x, y)
        #self.setIcon(QtGui.QIcon(directory))
        #self.setIconSize(self.size())
        #self.setMouseTracking(True)
        #self.setFlat(True)
        self.setMask(QtGui.QRegion(QtCore.QRect(-1, -1, x+2, y+2), QtGui.QRegion.Ellipse))
        self.setStyleSheet("CircleButton {border-image: url("+directory+");} CircleButton:hover {border-image: url("+directory_darker+");}")

class ToolButton(QtWidgets.QToolButton):
    def __init__(self, directory, x=48, y=58, parent=None):
        super(ToolButton, self).__init__(parent)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setFixedSize(x, y)
        self.setIcon(QtGui.QIcon(directory))
        self.setIconSize(self.size())
        self.setStyleSheet("ToolButton {background-color: transparent;}")
        #self.setStyleSheet("ToolButton {border-image: url(" + directory + ");} ToolButton:disabled {border: 0px solid red;} ToolButton:enabled {border: 10px solid red;} ToolButton:enabled:hover {border: 5px solid red;}")
