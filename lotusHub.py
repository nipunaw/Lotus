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

class UIHubWindow(QWidget):
    def __init__(self, parent=None):
        super(UIHubWindow, self).__init__(parent)

        ############ Lotus Logo ###########
        self.logo = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap('lotusAssets/lotusSmall.png')
        self.logo.setPixmap(self.pixmap)
        self.logo.show()

        ########### Buttons ###########
        self.new_note_button_display()
        self.schedule_button_display()
        self.previous_notes_button_display()

        ######### Grid Layout #########
        self.grid_layout()

    def new_note_button_display(self):
        self.new_note_button = QPushButton("", self)
        self.new_note_button.setGeometry(0, 0, 160, 160)
        # self.new_note_button.setFixedSize(160, 160)
        self.new_note_button.setIcon(QtGui.QIcon('lotusAssets/newNote.png'))
        self.new_note_button.setIconSize(self.new_note_button.size())
        # self.new_note_button.setMask(QtGui.QRegion(self.new_note_button.rect(), QtGui.QRegion.Ellipse))

    def schedule_button_display(self):
        self.schedule_button = QPushButton("", self)
        self.schedule_button.setGeometry(0, 0, 160, 160)
        # self.schedule_button.setFixedSize(160, 160)
        self.schedule_button.setIcon(QtGui.QIcon('lotusAssets/schedule.png'))
        self.schedule_button.setIconSize(self.schedule_button.size())

    def previous_notes_button_display(self):
        self.previous_notes_button = QPushButton("", self)
        self.previous_notes_button.setGeometry(0, 0, 160, 160)
        #self.previous_notes_button.setFixedSize(160, 160)
        self.previous_notes_button.setIcon(QtGui.QIcon('lotusAssets/previousNotes.png'))
        self.previous_notes_button.setIconSize(self.previous_notes_button.size())


    def grid_layout(self):
        ########### Set-Up Grid Layout ###########
        # initialize grid layout
        self.horizontalGroupBox = QtWidgets.QGroupBox()
        self.layout = QtWidgets.QGridLayout()

        # remove black outline border
        self.horizontalGroupBox.setFlat(True)
        self.horizontalGroupBox.setStyleSheet("border:0;")

        # add buttons to layout
        self.layout.addWidget(self.logo, 0, 1)
        self.layout.addWidget(self.new_note_button, 1, 0)
        self.layout.addWidget(self.schedule_button, 1, 1)
        self.layout.addWidget(self.previous_notes_button, 1, 2)

        # finish initializing grid layout
        self.horizontalGroupBox.setLayout(self.layout)
        self.windowLayout = QtWidgets.QVBoxLayout()
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(self.windowLayout)

        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(100)
        self.layout.setContentsMargins(200,200,200,300)

