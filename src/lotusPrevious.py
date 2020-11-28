# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

import json
import os

########### PyQT5 imports ###########
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton, QWidget

from src.constants import DIRECTORY_FILE, SCHEDULE_FILE_PATH, assets


class UIPreviousWindow(QWidget):
    def __init__(self, schedule, set_paths, parent=None):
        super(UIPreviousWindow, self).__init__(parent)
        self.set_paths = set_paths
        self.schedule = schedule
        # Creates file if not created
        try:
            file = open(DIRECTORY_FILE, 'r')
        except IOError:
            file = open(DIRECTORY_FILE, 'w')
        file.close()
        ############ Lotus Logo ###########
        #self.logo = QtWidgets.QLabel(self)
        #self.pixmap = QtGui.QPixmap('assets/lotusSmall.png')
        #self.logo.setPixmap(self.pixmap)
        #self.logo.show()
        #self.setFixedSize(600, 400)

        self.parent_layout = QtWidgets.QStackedWidget(self)
        self.parent_layout.setFixedSize(600, 400)

        self.home_button_container = QWidget()
        self.home_button_layout = QtWidgets.QVBoxLayout()
        self.home_button_container.setLayout(self.home_button_layout)

        self.all_button_container = QWidget()
        self.all_button_layout = QtWidgets.QVBoxLayout() # self #self.all_button_scroll
        self.all_button_container.setLayout(self.all_button_layout)

        self.home_button_scroll = QtWidgets.QScrollArea()  # self.home_button_container
        self.home_button_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.home_button_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.home_button_scroll.setWidgetResizable(True)
        self.home_button_scroll.setWidget(self.home_button_container)

        self.all_button_scroll = QtWidgets.QScrollArea() #self.all_button_container
        self.all_button_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.all_button_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.all_button_scroll.setWidgetResizable(True)
        self.all_button_scroll.setWidget(self.all_button_container)

        self.parent_layout.addWidget(self.home_button_scroll)
        self.parent_layout.addWidget(self.all_button_scroll)
        self.parent_layout.setCurrentIndex(0)

        # try:
        #     with open(SCHEDULE_FILE_PATH) as f:
        #         data = json.load(f)
        # except FileNotFoundError:
        #     data = []


        self.name_classes = []
        self.class_layouts = {}
        self.class_layouts_containers = {}
        self.class_layouts_scrolls = {}

        for (event_name, data) in self.schedule.schedule.items():
            event_type = data['type']
            if event_type == 'class' or event_type == 'recurring event':
                self.name_classes.append(event_name) ## Will this also catch one-time class events?
                self.class_layouts_containers[event_name] = QWidget()
                self.class_layouts[event_name] = QtWidgets.QVBoxLayout(self)
                self.class_layouts_containers[event_name].setLayout(self.class_layouts[event_name])
                self.class_layouts_scrolls[event_name] = QtWidgets.QScrollArea()
                self.class_layouts_scrolls[event_name].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                self.class_layouts_scrolls[event_name].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.class_layouts_scrolls[event_name].setWidgetResizable(True)
                self.class_layouts_scrolls[event_name].setWidget(self.class_layouts_containers[event_name])
                self.parent_layout.addWidget(self.class_layouts_scrolls[event_name])

        # for b in data:
        #     self.name_classes.append(b['name'])
        #     self.class_layouts_containers[b['name']] = QWidget()
        #     self.class_layouts[b['name']] = QtWidgets.QVBoxLayout(self)
        #     self.class_layouts_containers[b['name']].setLayout(self.class_layouts[b['name']])
        #     self.class_layouts_scrolls[b['name']] = QtWidgets.QScrollArea()
        #     self.class_layouts_scrolls[b['name']].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        #     self.class_layouts_scrolls[b['name']].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #     self.class_layouts_scrolls[b['name']].setWidgetResizable(True)
        #     self.class_layouts_scrolls[b['name']].setWidget(self.class_layouts_containers[b['name']])
        #     self.parent_layout.addWidget(self.class_layouts_scrolls[b['name']])

        self.home_ui()
        self.note_buttons()

    def home_ui(self):

        _id = QtGui.QFontDatabase.addApplicationFont(assets["lato"])

        button_style = "QPushButton {background-color: white; border: 1px solid #e1e1e1; text-align: left; font-size: 13px; font-family: Lato} QPushButton::hover {background-color: #e1e1e1;}"
        self.setStyleSheet(button_style)
        for i in self.name_classes:
            class_button = QtWidgets.QPushButton(i)
            class_button.setFixedHeight(30)
            #class_button.setFixedWidth(500)
            class_button.setStyleSheet(button_style)
            class_button.clicked.connect(lambda state, name=i: self.class_buttons(name))
            self.home_button_layout.addWidget(class_button)

        all_button = QtWidgets.QPushButton("All Notes")
        all_button.setFixedHeight(30)
        all_button.clicked.connect(self.all_notes)
        all_button.setStyleSheet(button_style)
        self.home_button_layout.addWidget(all_button)

        vertical_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.home_button_layout.addItem(vertical_spacer)

    def return_home(self):
        self.parent_layout.setCurrentIndex(0)

    def class_buttons(self, name):
        self.parent_layout.setCurrentWidget(self.class_layouts_scrolls[name])

    def all_notes(self):
        self.parent_layout.setCurrentIndex(1)

    def delete_button(self, str):
        for i in range(0, len(self.directories)):
            b : QPushButton = self.buttons[self.directories[i]]
            if b.text() == str:
                b.hide()

    def note_buttons(self):
        f = open(DIRECTORY_FILE, "r")
        self.read_directories = f.readlines()
        f.close()
        self.directories = []
        for i in self.read_directories:
            if os.path.isfile(i.strip()):
                self.directories.append(i)
        with open(DIRECTORY_FILE, "w") as f:
            f.writelines(p.strip() + "\n" for p in self.directories)


        back_button = QPushButton("Return Home")
        back_button.clicked.connect(self.return_home)
        self.all_button_layout.addWidget(back_button)

        for x in self.name_classes:
            back_button = QPushButton("Return Home")
            back_button.clicked.connect(self.return_home)
            self.class_layouts[x].addWidget(back_button)

        if len(self.directories) == 0:
            self.no_notes_text = QtWidgets.QLabel()
            self.no_notes_text.setText("No notes to display")
            self.all_button_layout.addWidget(self.no_notes_text)

        else:
            self.buttons = {}
            self.other_buttons = {}
            if not self.set_paths:
                for i in range(len(self.directories)):
                    self.buttons[self.directories[i]] = QPushButton(self.directories[i])
                    self.buttons[self.directories[i]].setIcon(QIcon(QPixmap(self.directories[i].strip())))
                    self.buttons[self.directories[i]].setIconSize(QSize(100,100))
                    self.all_button_layout.addWidget(self.buttons[self.directories[i]])

                    directory_array = self.directories[i].split('/')
                    if directory_array[-5] == "data" and directory_array[-4].isdigit() and directory_array[
                        -3].isdigit() and directory_array[-2].isdigit():
                        for x in self.name_classes:
                            if directory_array[-1].strip()[:-11] == x: ## Change for timestamp
                                self.other_buttons[self.directories[i]] = QPushButton(self.directories[i])
                                self.other_buttons[self.directories[i]].setIcon(QIcon(QPixmap(self.directories[i].strip())))
                                self.other_buttons[self.directories[i]].setIconSize(QSize(100, 100))
                                #self.all_button_layout.addWidget(self.other_buttons[self.directories[i]])
                                self.class_layouts[x].addWidget(self.other_buttons[self.directories[i]])
            else:
                for i in range(len(self.directories)):
                    self.buttons[self.directories[i]] = QPushButton(self.directories[i])
                    self.all_button_layout.addWidget(self.buttons[self.directories[i]])
        for x in self.name_classes:
            no_notes_text = QtWidgets.QLabel()
            no_notes_text.setText("No notes to display for this class/event")
            if self.class_layouts[x].count() == 1:
                self.no_notes_display(x, no_notes_text)
        self.add_spacer()

    def no_notes_display(self, x ,  widget):
        self.class_layouts[x].addWidget(widget)

    def add_spacer(self):
        for x in self.name_classes:
             vertical_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum,
                                                        QtWidgets.QSizePolicy.Expanding)
             self.class_layouts[x].addSpacerItem(vertical_spacer)
             #print(self.class_layouts[x].count())
        vertical_spacer_2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum,
                                                      QtWidgets.QSizePolicy.Expanding)
        self.all_button_layout.addSpacerItem(vertical_spacer_2)
