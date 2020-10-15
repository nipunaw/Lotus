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
from lotusButtons import CircleButton

class UIHubWindow(QWidget):
    def __init__(self, parent=None):
        super(UIHubWindow, self).__init__(parent)

        self.hubOpen = True

        ############ Lotus Logo ###########
        self.logo = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap('lotusAssets/lotus.png')
        self.logo.setPixmap(self.pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.show()

        ########### Buttons ###########
        self.new_note_button_display()
        self.schedule_button_display()
        self.previous_notes_button_display()

        ######### Grid Layout #########
        self.grid_layout()

    #def resizeEvent(self, event):
    #    self.new_note_button.setMask(QtGui.QRegion(self.rect(), QtGui.QRegion.Ellipse))
    #   QtWidgets.QPushButton.resizeEvent(self, event)

    def new_note_button_display(self):
        self.new_note_button = CircleButton("lotusAssets/newNote.png","lotusAssets/newNoteDarker.png")
        #self.new_note_button.setFixedSize(120, 120)
        #self.new_note_button.setIcon(QtGui.QIcon('lotusAssets/newNote.png'))
        #self.new_note_button.setIconSize(self.new_note_button.size())
        # self.new_note_button.setMask(QtGui.QRegion(self.new_note_button.rect(), QtGui.QRegion.Ellipse))
        #self.new_note_button.setStyleSheet("background-color: black")

    def schedule_button_display(self):
        self.schedule_button = CircleButton("lotusAssets/schedule.png", "lotusAssets/scheduleDarker.png")
        #self.schedule_button.setFixedSize(120, 120)
        #self.schedule_button.setIcon(QtGui.QIcon('lotusAssets/schedule.png'))
        #self.schedule_button.setIconSize(self.schedule_button.size())
        #self.schedule_button.setStyleSheet("background-color: black; padding-left: 100px; padding-right: 100px; text-align: center")

    def previous_notes_button_display(self):
        self.previous_notes_button = CircleButton("lotusAssets/previousNotes.png", "lotusAssets/previousNotesDarker.png")
        #self.previous_notes_button.setFixedSize(120, 120)
        #self.previous_notes_button.setIcon(QtGui.QIcon('lotusAssets/previousNotes.png'))
        #self.previous_notes_button.setIconSize(self.previous_notes_button.size())
        #self.previous_notes_button.setStyleSheet("background-color: black")

    def grid_layout(self):
        ########### Set-Up Grid Layout ###########
        # initialize grid layout
        self.horizontalGroupBox = QtWidgets.QGroupBox()
        self.layout = QtWidgets.QGridLayout()

        # remove black outline border
        self.horizontalGroupBox.setFlat(True)
        self.horizontalGroupBox.setStyleSheet("border:0;")

        # Text
        self.new_note_text = QtWidgets.QLabel()
        self.new_note_text.setText("New Note")
        self.new_note_text.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.schedule_text = QtWidgets.QLabel()
        self.schedule_text.setText("Schedule")
        self.schedule_text.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.previous_notes_text = QtWidgets.QLabel()
        self.previous_notes_text.setText("Previous Notes")
        self.previous_notes_text.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # add buttons to layout
        self.layout.addWidget(self.logo, 0, 1)
        self.layout.addWidget(self.new_note_button, 1, 0)
        self.layout.addWidget(self.new_note_text, 2, 0)
        self.layout.addWidget(self.schedule_button, 1, 1, Qt.AlignHCenter)
        self.layout.addWidget(self.schedule_text, 2, 1)
        self.layout.addWidget(self.previous_notes_button, 1, 2)
        self.layout.addWidget(self.previous_notes_text, 2, 2)

        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 0)
        self.layout.setColumnStretch(2, 0)

        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(10)
        #self.layout.setContentsMargins(100, 100, 100, 100)

        # finish initializing grid layout
        self.horizontalGroupBox.setLayout(self.layout)
        self.windowLayout = QtWidgets.QVBoxLayout()
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.windowLayout.setAlignment(Qt.AlignHCenter)
        self.setLayout(self.windowLayout)




