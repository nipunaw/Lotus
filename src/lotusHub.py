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
from src.constants import CONFIG_FILE, assets

class UIHubWindow(QWidget):
    def __init__(self, parent=None):
        super(UIHubWindow, self).__init__(parent)

        ## TODO: Add menu bar, and potentially add logo back

        ########### Logos ###########
        self.logo_ui()

        ########### Buttons ###########
        self.buttons_ui()

        ######## Text ###########
        self.text_ui()

        ######## Schedule ###########
        self.schedule_ui()

        ######### Date/Time ##########
        _id = QtGui.QFontDatabase.addApplicationFont(assets["lato"])
        self.time_date_display()
        self.counter = QtCore.QTimer(self)
        self.counter.setInterval(1000)
        self.counter.timeout.connect(self.time_date_display)
        self.counter.start()

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

    def logo_ui(self):
        self.logo_black = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap(assets["logo_black"])
        self.logo_black.setPixmap(self.pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def text_ui(self):
        self.new_note_text = QtWidgets.QLabel()
        self.new_note_text.setText("New Note")
        self.new_note_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.new_note_text.setStyleSheet("font-size: 13px; font-family: Lato")
        self.schedule_text = QtWidgets.QLabel()
        self.schedule_text.setText("Schedule")
        self.schedule_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.schedule_text.setStyleSheet("font-size: 13px; font-family: Lato")
        self.previous_notes_text = QtWidgets.QLabel()
        self.previous_notes_text.setText("Previous Notes")
        self.previous_notes_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.previous_notes_text.setStyleSheet("font-size: 13px; font-family: Lato")
        self.no_schedule_text = QtWidgets.QLabel()
        self.no_schedule_text.setText("No upcoming classes.")
        self.no_schedule_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.no_schedule_text.setStyleSheet("font-size: 15px; font-family: Lato")
        self.time = QtWidgets.QLabel()
        self.date = QtWidgets.QLabel()
        self.time.setStyleSheet("color: white; font-size: 35px; font-family: Lato")
        self.date.setStyleSheet("color: white; font-size: 15px; font-family: Lato")
        self.time.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.date.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

    def buttons_ui(self):
        self.new_note_button = CircleButton(assets["newNote"], assets["newNoteDarker"])
        self.schedule_button = CircleButton(assets["schedule"], assets["scheduleDarker"])
        self.previous_notes_button = CircleButton(assets["previousNotes"], assets["previousNotesDarker"])
        self.settings_button = CircleButton(assets["settings"], assets["settings"], 20, 20)
        self.help_button = CircleButton(assets["help"], assets["help"], 20, 20)

    def menu_ui(self):
        self.menu_background = QtWidgets.QLabel(self)
        self.menu_background.setGeometry(0, 0, 800, 43)
        self.menu_background.setStyleSheet("background-color: #f2f2f5")
        self.menu_bar = QtWidgets.QLabel()
        self.menu_bar.setGeometry(0, 0, 800, 48) # should set width (=800) dynamically
        self.menu_bar.setStyleSheet("background-color: #f2f2f5")
        self.user_welcome = QtWidgets.QLabel()
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        self.user_welcome.setText("Welcome back " + config['DEFAULT']['name'])
        self.user_welcome.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.user_welcome.setStyleSheet("font-family: Lato")

    def time_date_display(self):
        self.time.setText(QtCore.QTime.currentTime().toString())
        self.date.setText(QtCore.QDate.currentDate().toString())

    def schedule_ui(self):
        self.schedule_background = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap(assets["time_date"])
        self.schedule_background.setPixmap(self.pixmap.scaled(610, 451, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    #def new_note_button_display(self):
        #self.new_note_button.setFixedSize(120, 120)
        #self.new_note_button.setIcon(QtGui.QIcon('assets/newNote.png'))
        #self.new_note_button.setIconSize(self.new_note_button.size())
        # self.new_note_button.setMask(QtGui.QRegion(self.new_note_button.rect(), QtGui.QRegion.Ellipse))
        #self.new_note_button.setStyleSheet("background-color: black")

   # def schedule_button_display(self):
        #self.schedule_button.setFixedSize(120, 120)
        #self.schedule_button.setIcon(QtGui.QIcon('assets/schedule.png'))
        #self.schedule_button.setIconSize(self.schedule_button.size())
        #self.schedule_button.setStyleSheet("background-color: black; padding-left: 100px; padding-right: 100px; text-align: center")

    #def previous_notes_button_display(self):
        #self.previous_notes_button.setFixedSize(120, 120)
        #self.previous_notes_button.setIcon(QtGui.QIcon('assets/previousNotes.png'))
        #self.previous_notes_button.setIconSize(self.previous_notes_button.size())
        #self.previous_notes_button.setStyleSheet("background-color: black")

    def welcome_screen(self):
        self.logo = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap(assets["logo"])
        self.logo.setPixmap(self.pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.move(275,120)
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

        self.animation_ui(1)

    def confirm(self):
        if self.line.text() != '':
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            config.set("DEFAULT", "name", self.line.text())
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
            self.animation_ui(2)
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

    def animation_ui(self, flag):
        if flag == 1:
            self.fade_1 = Animations.fade_in(self, self.welcome_text)
            self.fade_2 = Animations.fade_in(self, self.line)
            self.fade_3 = Animations.fade_in(self, self.confirm_button)
            self.fade_logo = Animations.fade_in(self, self.logo)
            self.animationGroup_1 = QtCore.QParallelAnimationGroup()
            self.animationGroup_1.addAnimation(self.fade_1)
            self.animationGroup_1.addAnimation(self.fade_2)
            self.animationGroup_1.addAnimation(self.fade_3)
            self.animationGroup_1.addAnimation(self.fade_logo)
            self.animationGroup_1.start()
        elif flag == 2:
            self.fade_4 = Animations.fade_out(self, self.welcome_text)
            self.fade_5 = Animations.fade_out(self, self.line)
            self.fade_6 = Animations.fade_out(self, self.confirm_button)
            self.fade_out_logo = Animations.fade_out(self, self.logo)
            self.animationGroup_2 = QtCore.QParallelAnimationGroup()
            self.animationGroup_2.addAnimation(self.fade_4)
            self.animationGroup_2.addAnimation(self.fade_5)
            self.animationGroup_2.addAnimation(self.fade_6)
            self.animationGroup_2.addAnimation(self.fade_out_logo)
            self.animationGroup_2.start()
        else:
            self.fade_7 = Animations.fade_in(self, self.new_note_button)
            self.fade_8 = Animations.fade_in(self, self.schedule_button)
            self.fade_9 = Animations.fade_in(self, self.previous_notes_button)
            self.fade_10 = Animations.fade_in(self, self.schedule_background)
            self.fade_11 = Animations.fade_in(self, self.new_note_text)
            self.fade_12 = Animations.fade_in(self, self.schedule_text)
            self.fade_13 = Animations.fade_in(self, self.previous_notes_text)
            self.fade_14 = Animations.fade_in(self, self.user_welcome)
            self.animationGroup_3 = QtCore.QParallelAnimationGroup()
            self.animationGroup_3.addAnimation(self.fade_7)
            self.animationGroup_3.addAnimation(self.fade_8)
            self.animationGroup_3.addAnimation(self.fade_9)
            self.animationGroup_3.addAnimation(self.fade_10)
            self.animationGroup_3.addAnimation(self.fade_11)
            self.animationGroup_3.addAnimation(self.fade_12)
            self.animationGroup_3.addAnimation(self.fade_13)
            self.animationGroup_3.addAnimation(self.fade_14)
            self.animationGroup_3.start()

    def grid_layout(self):
            ########### Menu Bar ###########
            self.menu_ui()

            ########### Set-Up Grid Layout ###########
            # initialize grid layout
            self.horizontalGroupBox = QtWidgets.QGroupBox()
            self.layout = QtWidgets.QGridLayout()

            # remove black outline border
            self.horizontalGroupBox.setFlat(True)
            self.horizontalGroupBox.setStyleSheet("border:0;")

            # add buttons to layout
            self.layout.addWidget(self.menu_bar, 0,0,1,4)
            self.layout.addWidget(self.user_welcome, 0, 1)
            self.layout.addWidget(self.logo_black, 0, 0)
            self.layout.addWidget(self.settings_button, 0, 3, Qt.AlignRight)
            self.layout.addWidget(self.help_button, 0, 2, Qt.AlignRight)
            self.layout.addWidget(self.schedule_background, 1, 0, 6, 3) # Qt.AlignLeft
            self.layout.addWidget(self.time, 1, 1)
            self.layout.addWidget(self.date, 1, 1)
            self.layout.addWidget(self.no_schedule_text, 4, 1) ## TODO: Add boolean logic
            self.layout.addWidget(self.new_note_button, 1, 3)
            self.layout.addWidget(self.new_note_text, 2, 3)
            self.layout.addWidget(self.schedule_button, 3, 3) # Qt.AlignHCenter
            self.layout.addWidget(self.schedule_text, 4, 3)
            self.layout.addWidget(self.previous_notes_button, 5, 3)
            self.layout.addWidget(self.previous_notes_text, 6, 3)

            # self.layout.setColumnStretch(0, 0)
            # self.layout.setColumnStretch(1, 0)
            # self.layout.setColumnStretch(2, 0)

            self.layout.setHorizontalSpacing(30)
            self.layout.setVerticalSpacing(5)
            self.layout.setContentsMargins(0, 0, 0, 0)

            # finish initializing grid layout
            self.horizontalGroupBox.setLayout(self.layout)
            self.windowLayout = QtWidgets.QVBoxLayout()
            self.windowLayout.addWidget(self.horizontalGroupBox)
            self.windowLayout.setAlignment(Qt.AlignHCenter)

            self.setLayout(self.windowLayout)

            self.animation_ui(3)
