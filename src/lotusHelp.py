# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QScrollArea, QVBoxLayout, \
    QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal
import configparser
from src.constants import CONFIG_FILE, assets

class UIHelpWindow(QWidget):

    def __init__(self, parent=None):
        super(UIHelpWindow, self).__init__(parent)
        #self.setMinimumWidth(320)
        self.field_ui()

    def field_ui(self):
        # Container Widget
        self.widget = QWidget()
        # Layout of Container Widget
        self.layout = QVBoxLayout(self)

        self.label = QLabel('Help Page')
        self.label.setFont(QFont('Arial', 20))
        self.label.adjustSize()
        self.layout.addWidget(self.label)

        self.label_2 = QLabel('Welcome to Lotus. This Help Page will introduce you to the main features of the Lotus Notes tool.')
        self.label_2.setFont(QFont('Arial', 9))
        self.label_2.setWordWrap(True)
        self.label_2.adjustSize()
        self.layout.addWidget(self.label_2)

        self.pixmap = QPixmap(assets["help_lotus_home"])
        self.pixmap = self.pixmap.scaled(300, 300)
        self.label_3 = QLabel(self)
        self.label_3.setPixmap(self.pixmap)
        self.label_3.adjustSize()
        self.layout.addWidget(self.label_3)

        self.label_4 = QLabel('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.label_4.setFont(QFont('Arial', 9))
        self.label_4.setWordWrap(True)
        self.label_4.adjustSize()
        self.layout.addWidget(self.label_4)

        self.label_5 = QLabel('Welcome to Lotus. This Help Page will introduce you to the main features of the Lotus Notes tool. On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.label_5.setFont(QFont('Arial', 9))
        self.label_5.setWordWrap(True)
        self.label_5.adjustSize()
        self.layout.addWidget(self.label_5)

        self.label_6 = QLabel('Welcome to Lotus. This Help Page will introduce you to the main features of the Lotus Notes tool. On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.label_6.setFont(QFont('Arial', 9))
        self.label_6.setWordWrap(True)
        self.label_6.adjustSize()
        self.layout.addWidget(self.label_6)

        self.label_7 = QLabel(
            'Welcome to Lotus. This Help Page will introduce you to the main features of the Lotus Notes tool. On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.label_7.setFont(QFont('Arial', 9))
        self.label_7.setWordWrap(True)
        self.label_7.adjustSize()
        self.layout.addWidget(self.label_7)

        self.label_8 = QLabel(
            'Welcome to Lotus. This Help Page will introduce you to the main features of the Lotus Notes tool. On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.label_8.setFont(QFont('Arial', 9))
        self.label_8.setWordWrap(True)
        self.label_8.adjustSize()
        self.layout.addWidget(self.label_8)

        self.widget.setLayout(self.layout)

        # Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(self.widget)

        # Scroll Area Layer add
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.scroll)
        self.setLayout(self.vLayout)

