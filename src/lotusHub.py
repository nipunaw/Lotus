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
import itertools
import json
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from src.lotusButtons import CircleButton
import configparser
from src.lotusAnimations import Animations
from src.lotusCalender import Schedule, ScheduleCalendar
from src.constants import CONFIG_FILE, assets, SCHEDULE_FILE_PATH
from src.lotusUtils import clear_layout

class UpcomingClasses(QWidget):
    buttons_updated = pyqtSignal(list)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    def __init__(self, schedule:Schedule):
        super(UpcomingClasses, self).__init__()
        self.schedule = schedule
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 30, 0, 10)
        # self.setStyleSheet("background: black")
        self.no_schedule_text = QtWidgets.QLabel()
        self.no_schedule_text.setText("No upcoming classes.")
        self.no_schedule_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.no_schedule_text.setStyleSheet("font-size: 15px; font-family: Lato")

        self.scope = 0
        self.scopes = ["Day", "Week", "Month"]
        self.current_date = QtCore.QDate.currentDate()
        self.viewing_date = QtCore.QDate.currentDate()
        scope_selector = QPushButton(self.scopes[self.scope], self)
        scope_selector.setFlat(True)
        scope_menu = QtWidgets.QMenu()
        scope_menu.aboutToShow.connect(lambda: scope_menu.setMinimumWidth(scope_selector.width()))
        for scope in self.scopes:
            # action = QtWidgets.QAction(scope, scope_menu)
            action = QtWidgets.QAction(scope, scope_menu)
            action.triggered.connect(lambda state, x=len(scope_menu.actions()), y=scope_selector: self.scope_action(x, y))
            scope_menu.addAction(action)
        scope_selector.setMenu(scope_menu)

        left_button = QPushButton("<", self)
        left_button.setMaximumWidth(15)
        left_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        left_button.clicked.connect(lambda state, x=-1: self.update_date(x))

        right_button = QPushButton(">", self)
        right_button.setMaximumWidth(15)
        right_button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        right_button.clicked.connect(lambda state, x=1: self.update_date(x))

        self.header = QtWidgets.QLabel(self.get_header(self.viewing_date))
        self.header.setStyleSheet("color: black; font-size: 16px; font-family: Lato")

        self.stack = QtWidgets.QStackedWidget()
        self.calendar = ScheduleCalendar(self.schedule, self.stack, parent=self)
        self.stack.addWidget(self.calendar)
        self.calendar.currentPageChanged.connect(
            lambda state, _: self.calendar.setCurrentPage(self.viewing_date.year(), self.viewing_date.month()))
        self.calendar.setCurrentPage(self.viewing_date.year(), self.viewing_date.month())

        self.scope_viewer = QtWidgets.QGridLayout()
        self.scope_viewer.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.update_scope_viewer()

        middle_layout = QtWidgets.QVBoxLayout()
        middle_layout.setAlignment(Qt.AlignTop | Qt.AlignVCenter)
        middle_layout.addWidget(scope_selector, alignment=Qt.AlignTop | Qt.AlignVCenter)
        middle_layout.addWidget(self.header, alignment=Qt.AlignCenter | Qt.AlignTop)
        middle_layout.addLayout(self.scope_viewer)

        self.layout.addWidget(left_button, Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.addLayout(middle_layout, Qt.AlignTop | Qt.AlignVCenter)
        self.layout.addWidget(right_button, Qt.AlignRight | Qt.AlignVCenter)
        # self.layout.addWidget(self.no_schedule_text)
        self.setLayout(self.layout)

    def update_date(self, direction):
        if direction != 0:
            if self.scope == 0:
                self.viewing_date = self.viewing_date.addDays(direction)
            elif self.scope == 1:
                self.viewing_date = self.viewing_date.addDays(7 * direction)
            elif self.scope == 2:
                self.viewing_date = self.viewing_date.addMonths(direction)
        self.header.setText(self.get_header(self.viewing_date))
        self.calendar.setCurrentPage(self.viewing_date.year(), self.viewing_date.month())
        self.update_scope_viewer()

    def get_first_and_last_day_of_week(self, date:QDate):
        start_date = date
        while start_date.dayOfWeek() != 1:
            start_date = start_date.addDays(-1)
        end_date = start_date.addDays(6)
        return start_date, end_date

    def get_header(self, date):
        day_of_week = self.days[date.dayOfWeek()-1]
        if self.scope == 0:
            return "{}{}, {}".format("Today, " if self.current_date == self.viewing_date else "", day_of_week, date.toString("MMMM d"))
        elif self.scope == 1:
            # Get previous Monday
            start_date, end_date = self.get_first_and_last_day_of_week(date)
            return "{}, {} - {}, {}".format(self.days[start_date.dayOfWeek()-1], start_date.toString("MMM d"), self.days[end_date.dayOfWeek()-1], end_date.toString("MMM d"))
        elif self.scope == 2:
            return date.toString("MMMM")

    def scope_action(self, new_scope:int, parent:QPushButton):
        if self.scope == new_scope:
            return
        self.scope = new_scope
        parent.setText(self.scopes[self.scope])
        self.update_date(0)

    def update_scope_viewer(self):
        clear_layout(self.scope_viewer, [self.calendar, self.stack])
        if self.scope == 0:
            button_layout = QtWidgets.QVBoxLayout()
            for button, _, _, _ in self.schedule.get_event_buttons(self.viewing_date):
                button_layout.addWidget(button)
            self.scope_viewer.addLayout(button_layout, 0, 0, self.scope_viewer.rowCount(), self.scope_viewer.columnCount())
        elif self.scope == 1:
            layout = QtWidgets.QGridLayout()
            layout.setSpacing(10)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            scroll_area = QtWidgets.QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(layout.widget())
            scroll_area.setLayout(layout)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            start_date, end_date = self.get_first_and_last_day_of_week(self.viewing_date)
            week = []
            while start_date <= end_date:
                week.append(start_date)
                start_date = start_date.addDays(1)
            for i, (name, date) in enumerate(zip(self.days, week)):
                buttons = self.schedule.get_event_buttons(date)
                if len(buttons) > 0:
                    name_label = QtWidgets.QLabel(name)
                    name_label.setAlignment(Qt.AlignCenter)
                    layout.addWidget(name_label, 0, i)
                    for j, (button, _, _, _) in enumerate(buttons):
                        layout.addWidget(button, j+1, i)
                self.scope_viewer.addWidget(scroll_area)
        elif self.scope == 2:
            if self.calendar.day_viewer is not None:
                self.stack.removeWidget(self.calendar.day_viewer)
            self.stack.show()
            self.calendar.show()
            for child in self.calendar.children():
                if child.__class__ is not QtWidgets.QTableView:
                    try:
                        child.hide()
                    except Exception as e:
                        continue
            self.scope_viewer.addWidget(self.stack)

class UIHubWindow(QWidget):
    def __init__(self, schedule:Schedule, parent=None):
        super(UIHubWindow, self).__init__(parent)

        ## TODO: Add menu bar, and potentially add logo back

        self.schedule = schedule

        ########### Buttons ###########
        self.buttons_ui()

        ######## Other Text ###########
        self.text_ui()

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
        self.time = QtWidgets.QLabel(self)
        self.date = QtWidgets.QLabel(self)
        self.time.setStyleSheet("color: white; font-size: 35px; font-family: Lato")
        self.date.setStyleSheet("color: white; font-size: 15px; font-family: Lato")
        self.time.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.date.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

    def buttons_ui(self):
        self.new_note_button = CircleButton(assets["newNote"], assets["newNoteDarker"])
        self.schedule_button = CircleButton(assets["schedule"], assets["scheduleDarker"])
        self.previous_notes_button = CircleButton(assets["previousNotes"], assets["previousNotesDarker"])


    def time_date_display(self):
        self.time.setText(QtCore.QTime.currentTime().toString())
        self.date.setText(QtCore.QDate.currentDate().toString())

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

        self.animation_ui(1)

    def confirm(self):
        if self.line.text() != '':
            file = open(CONFIG_FILE, 'w')
            config = configparser.ConfigParser()
            config['DEFAULT'] = {'Name': self.line.text()}
            config.write(file)

            self.animation_ui(2)
            self.fade_6.finished.connect(self.grid_layout)

    def animation_ui(self, flag):
        if flag == 1:
            self.fade_1 = Animations.fade_in(self, self.welcome_text)
            self.fade_2 = Animations.fade_in(self, self.line)
            self.fade_3 = Animations.fade_in(self, self.confirm_button)
            self.animationGroup_1 = QtCore.QParallelAnimationGroup()
            self.animationGroup_1.addAnimation(self.fade_1)
            self.animationGroup_1.addAnimation(self.fade_2)
            self.animationGroup_1.addAnimation(self.fade_3)
            self.animationGroup_1.start()
        elif flag == 2:
            self.fade_4 = Animations.fade_out(self, self.welcome_text)
            self.fade_5 = Animations.fade_out(self, self.line)
            self.fade_6 = Animations.fade_out(self, self.confirm_button)
            self.animationGroup_2 = QtCore.QParallelAnimationGroup()
            self.animationGroup_2.addAnimation(self.fade_4)
            self.animationGroup_2.addAnimation(self.fade_5)
            self.animationGroup_2.addAnimation(self.fade_6)
            self.animationGroup_2.start()
        else:
            self.fade_7 = Animations.fade_in(self, self.new_note_button)
            self.fade_8 = Animations.fade_in(self, self.schedule_button)
            self.fade_9 = Animations.fade_in(self, self.previous_notes_button)
            self.fade_10 = Animations.fade_in(self, self.schedule_background)
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

    def grid_layout(self):
            ############ Lotus Logo ###########
            self.schedule_background = QtWidgets.QLabel(self)
            self.pixmap = QtGui.QPixmap(assets["time_date"])
            self.schedule_background.setPixmap(self.pixmap.scaled(610, 451, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            ########### Set-Up Grid Layout ###########
            # initialize grid layout
            self.horizontal_layout = QtWidgets.QHBoxLayout()
            self.layout = QtWidgets.QGridLayout()

            self.upcoming_classes = UpcomingClasses(self.schedule)

            # add buttons to layout
            self.layout.addWidget(self.schedule_background, 0, 0, 6, 3) # Qt.AlignLeft
            self.layout.addWidget(self.time, 0, 1)
            self.layout.addWidget(self.date, 0, 1)
            self.layout.addWidget(self.upcoming_classes, 2, 0, 4, 3) ## TODO: Add boolean logic
            self.layout.addWidget(self.new_note_button, 0, 3)
            self.layout.addWidget(self.new_note_text, 1, 3)
            self.layout.addWidget(self.schedule_button, 2, 3) # Qt.AlignHCenter
            self.layout.addWidget(self.schedule_text, 3, 3)
            self.layout.addWidget(self.previous_notes_button, 4, 3)
            self.layout.addWidget(self.previous_notes_text, 5, 3)

            self.layout.setColumnStretch(0, 0)
            self.layout.setColumnStretch(1, 0)
            self.layout.setColumnStretch(2, 0)

            self.layout.setHorizontalSpacing(30)
            self.layout.setVerticalSpacing(0)
            #self.layout.setContentsMargins(100, 100, 100, 100)

            # finish initializing grid layout
            self.horizontal_layout.addLayout(self.layout)
            self.windowLayout = QtWidgets.QVBoxLayout()
            self.windowLayout.addLayout(self.horizontal_layout)
            self.windowLayout.setAlignment(Qt.AlignHCenter)
            self.schedule_background.lower()
            self.upcoming_classes.lower()
            self.setLayout(self.windowLayout)

            self.animation_ui(3)

