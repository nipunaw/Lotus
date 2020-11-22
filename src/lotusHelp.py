# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5.QtGui import QFont, QPixmap, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QScrollArea, QVBoxLayout, \
    QSizePolicy, QTextEdit
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal
import configparser
from src.constants import CONFIG_FILE, assets

class UIHelpWindow(QWidget):
    def __init__(self, parent=None):
        super(UIHelpWindow, self).__init__(parent)
        self.setMinimumWidth(320)
        self.help_ui()

    def insertImageFunc(self, filepath, cursor):
        # grab image
        reader = QtGui.QImageReader(filepath)
        image = reader.read()

        # resize image
        resizedImage = image.scaled(400, 400, QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # move the cursor
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        # add image
        cursor.insertImage(resizedImage)


    def help_ui(self):
        #self.mainLayout = QVBoxLayout()
        self.helpTextEditor = QTextEdit()
        self.helpTextEditor.setWindowTitle("Help")
        self.helpTextEditor.setMinimumSize(800,500)
        #self.mainLayout.addWidget(self.helpTextEditor)

        self.helpTextEditor.setReadOnly(True)

        self.helpTextEditor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.document = self.helpTextEditor.document()
        self.cursor = QTextCursor(self.document)

        self.helpTextEditor.setCurrentFont(QFont('Arial'))
        self.helpTextEditor.setFontUnderline(True)
        self.helpTextEditor.setFontPointSize(48)
        self.helpTextEditor.setText('Help')

        self.helpTextEditor.setCurrentFont(QFont('Arial'))
        self.helpTextEditor.setFontUnderline(False)
        self.helpTextEditor.setFontPointSize(10)

        self.helpTextEditor.append('\nWelcome to Lotus. This Help Page will introduce you to the main features of the Lotus Notes tool. \n')

        self.insertImageFunc(assets["help_lotus_home"], self.cursor)
        self.helpTextEditor.append('\n')

        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')
        self.helpTextEditor.append('On the main hub screen, there are the three main options: (1) New Note, (2) Schedule, and (3) Previous Notes.')

        self.helpTextEditor.moveCursor(QtGui.QTextCursor.Start)
        self.helpTextEditor.show()
        #self.setLayout(self.mainLayout)