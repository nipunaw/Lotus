# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5 import QtCore, QtGui, QtWidgets

class CircleButton(QtWidgets.QPushButton):
    def __init__(self, directory, directory_darker, parent=None):
        super(CircleButton, self).__init__(parent)
        self.setFixedSize(120, 120)
        #self.setIcon(QtGui.QIcon(directory))
        #self.setIconSize(self.size())
        #self.setMouseTracking(True)
        self.setMask(QtGui.QRegion(QtCore.QRect(-1, -1, 122, 122), QtGui.QRegion.Ellipse))
        self.setStyleSheet("CircleButton {border-image: url("+directory+");} CircleButton:hover {border-image: url("+directory_darker+");}")