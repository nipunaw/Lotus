# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QGroupBox, QGridLayout, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor


class UIHubWindow(QWidget):
    def __init__(self, parent=None):
        super(UIHubWindow, self).__init__(parent)

        ########### Add Logo ###########
        # Create widget
        logo = QLabel(self)
        pixmap = QPixmap('logo_small.png')
        logo.setPixmap(pixmap)
        logo.show()

        ########### Add Buttons ###########
        # create buttons
        self.scheduled_notes_button = QPushButton("Scheduled Notes", self)
        self.new_note_button = QPushButton("New Note", self)
        self.other_notes_button = QPushButton("Other Notes", self)

        # change font of text in buttons
        self.scheduled_notes_button.setFont(QFont('Times', 15))
        self.new_note_button.setFont(QFont('Times', 15))
        self.other_notes_button.setFont(QFont('Times', 15))

        # change color of text in buttons
        palette = QPalette(self.scheduled_notes_button.palette())  # make a copy of the palette
        palette.setColor(QPalette.ButtonText, QColor('White'))
        self.scheduled_notes_button.setPalette(palette)  # assign new palette

        palette = QPalette(self.new_note_button.palette())  # make a copy of the palette
        palette.setColor(QPalette.ButtonText, QColor('White'))
        self.new_note_button.setPalette(palette)  # assign new palette

        palette = QPalette(self.other_notes_button.palette())  # make a copy of the palette
        palette.setColor(QPalette.ButtonText, QColor('White'))
        self.other_notes_button.setPalette(palette)  # assign new palette

        # set icons for buttons
        self.scheduled_notes_button.setIcon(QtGui.QIcon('scheduled_notes_small.png'))
        self.new_note_button.setIcon(QtGui.QIcon('new_note_small.png'))
        self.other_notes_button.setIcon(QtGui.QIcon('other_notes_small.png'))

        # resize icons
        self.scheduled_notes_button.setIconSize(self.scheduled_notes_button.size())
        self.new_note_button.setIconSize(self.new_note_button.size())
        self.other_notes_button.setIconSize(self.other_notes_button.size())

        # add hover white border
        self.scheduled_notes_button.setStyleSheet("QPushButton::hover {border: 1px solid white;}")
        self.new_note_button.setStyleSheet("QPushButton::hover {border : 1px solid white;}")
        self.other_notes_button.setStyleSheet("QPushButton::hover {border : 1px solid white;}")

        ########### Set-Up Grid Layout ###########
        # initialize grid layout
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        # remove black outline border
        self.horizontalGroupBox.setFlat(True)
        self.horizontalGroupBox.setStyleSheet("border:0;")

        # add buttons to layout
        layout.addWidget(self.new_note_button, 1, 0)
        layout.addWidget(self.scheduled_notes_button, 1, 1)
        layout.addWidget(self.other_notes_button, 1, 2)

        # finish initializing grid layout
        self.horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

        # self.scheduled_notes_button = QPushButton("Scheduled Notes", self)
        # self.other_notes_button = QPushButton("Other Notes", self)

        # self.new_note_button = QPushButton("New Note", self)
        # self.new_note_button.move(750, 480)

        ########### CSS Stylesheet (experimental) ###########
        #self.setStyleSheet("""
        #        QLabel {
        #                color: white;
        #        }
        #        QPushButton {
        #            	background-color:#44c767;
        #                border-radius:28px;
        #                border:1px solid #18ab29;
        #                color:#ffffff;
        #                font-family:Arial;
        #                font-size:17px;
        #                text-decoration:none;
        #             }
        #         QPushButton:hover {
        #                background-color: #3db35c;
        #        }
        #        """)
