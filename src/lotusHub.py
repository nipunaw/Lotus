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
from src.lotusButtons import CircleButton
import configparser
from src.lotusAnimations import Animations

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/config.ini')

class UIHubWindow(QWidget):
    def __init__(self, parent=None):
        super(UIHubWindow, self).__init__(parent)

        self.logo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/lotus.png')
        self.new_notes_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/newNote.png')
        self.new_notes_darker_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                  'assets/newNoteDarker.png')
        self.previous_notes_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/previousNotes.png')
        self.previous_notes_darker_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                       'assets/previousNotesDarker.png')
        self.schedule_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/schedule.png')
        self.schedule_darker_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                 'assets/scheduleDarker.png')

        ########### Buttons ###########
        self.new_note_button_display()
        self.schedule_button_display()
        self.previous_notes_button_display()

        ######### Grid Layout #########
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        if config['DEFAULT']['name'] == '':
            self.welcome_screen()
        else:
            self.grid_layout()

    #def resizeEvent(self, event):
    #    self.new_note_button.setMask(QtGui.QRegion(self.rect(), QtGui.QRegion.Ellipse))
    #   QtWidgets.QPushButton.resizeEvent(self, event)

    def new_note_button_display(self):
        self.new_note_button = CircleButton(self.new_notes_path, self.new_notes_darker_path)
        #self.new_note_button.setFixedSize(120, 120)
        #self.new_note_button.setIcon(QtGui.QIcon('assets/newNote.png'))
        #self.new_note_button.setIconSize(self.new_note_button.size())
        # self.new_note_button.setMask(QtGui.QRegion(self.new_note_button.rect(), QtGui.QRegion.Ellipse))
        #self.new_note_button.setStyleSheet("background-color: black")

    def schedule_button_display(self):
        self.schedule_button = CircleButton(self.schedule_path, self.schedule_darker_path)
        #self.schedule_button.setFixedSize(120, 120)
        #self.schedule_button.setIcon(QtGui.QIcon('assets/schedule.png'))
        #self.schedule_button.setIconSize(self.schedule_button.size())
        #self.schedule_button.setStyleSheet("background-color: black; padding-left: 100px; padding-right: 100px; text-align: center")

    def previous_notes_button_display(self):
        self.previous_notes_button = CircleButton(self.previous_notes_path, self.previous_notes_darker_path)
        #self.previous_notes_button.setFixedSize(120, 120)
        #self.previous_notes_button.setIcon(QtGui.QIcon('assets/previousNotes.png'))
        #self.previous_notes_button.setIconSize(self.previous_notes_button.size())
        #self.previous_notes_button.setStyleSheet("background-color: black")

    def welcome_screen(self):
        self.welcome_text = QtWidgets.QLabel(self)
        self.welcome_text.setText("Welcome to Lotus. Please enter your name:")
        self.welcome_text.move(250, 200)
        self.line = QtWidgets.QLineEdit(self)

        self.line.move(250, 240)
        self.line.resize(250, 32)

        self.confirm_button = QPushButton('Confirm', self)
        self.confirm_button.resize(200, 32)
        self.confirm_button.move(275, 290)
        self.confirm_button.clicked.connect(self.confirm)

        self.fade_1 = Animations.fade_in(self, self.welcome_text)
        self.fade_2 = Animations.fade_in(self, self.line)
        self.fade_3 = Animations.fade_in(self, self.confirm_button)
        self.animationGroup_1 = QtCore.QParallelAnimationGroup()
        self.animationGroup_1.addAnimation(self.fade_1)
        self.animationGroup_1.addAnimation(self.fade_2)
        self.animationGroup_1.addAnimation(self.fade_3)
        self.animationGroup_1.start()

    def confirm(self):
        if self.line.text() != '':
            file = open(CONFIG_FILE, 'w')
            config = configparser.ConfigParser()
            config['DEFAULT'] = {'Name': self.line.text()}
            config.write(file)

            self.fade_4 = Animations.fade_out(self, self.welcome_text)
            self.fade_5 = Animations.fade_out(self, self.line)
            self.fade_6 = Animations.fade_out(self, self.confirm_button)
            self.animationGroup_2 = QtCore.QParallelAnimationGroup()
            self.animationGroup_2.addAnimation(self.fade_4)
            self.animationGroup_2.addAnimation(self.fade_5)
            self.animationGroup_2.addAnimation(self.fade_6)
            self.animationGroup_2.start()

            self.fade_6.finished.connect(self.grid_layout)

    # def startup(self):
    #     config = configparser.ConfigParser()
    #     config.read(CONFIG_FILE)
    #     self.hello_text = QtWidgets.QLabel(self)
    #     self.hello_text.setText("Hello, "+ config['DEFAULT']['name'])
    #     self.hello_text.move(250, 250)
    #
    #     self.fade_14 = Animations.fade_in(self, self.hello_text)
    #     self.fade_14.start()
    #     self.fade_14.finished.connect(self.startup_finished)
    #
    # def startup_finished(self):
    #     self.fade_15 = Animations.fade_out(self, self.hello_text)
    #     self.fade_15.start()
    #     self.fade_15.finished.connect(self.grid_layout)

    def grid_layout(self):
            ############ Lotus Logo ###########
            self.logo = QtWidgets.QLabel(self)
            self.pixmap = QtGui.QPixmap(self.logo_path)
            self.logo.setPixmap(self.pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

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

            self.fade_7 = Animations.fade_in(self, self.new_note_button)
            self.fade_8 = Animations.fade_in(self, self.schedule_button)
            self.fade_9 = Animations.fade_in(self, self.previous_notes_button)
            self.fade_10 = Animations.fade_in(self, self.logo)
            self.fade_11 = Animations.fade_in(self, self.new_note_text)
            self.fade_12 = Animations.fade_in(self, self.schedule_text)
            self.fade_13 = Animations.fade_in(self, self.previous_notes_text)
            self.animationGroup_3 = QtCore.QParallelAnimationGroup()
            self.animationGroup_3.addAnimation(self.fade_7)
            self.animationGroup_3.addAnimation(self.fade_8)
            self.animationGroup_3.addAnimation(self.fade_9)
            self.animationGroup_3.addAnimation(self.fade_10)
            self.animationGroup_3.addAnimation(self.fade_11)
            self.animationGroup_3.addAnimation(self.fade_12)
            self.animationGroup_3.addAnimation(self.fade_13)
            self.animationGroup_3.start()

            self.setLayout(self.windowLayout)

