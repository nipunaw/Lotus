# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### WSL import ###########
import wsl
########### PyQT5 imports ###########
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
########### File imports ###########
from lotusHub import UIHubWindow
from lotusNotes import UINoteWindow
from lotusCalender import UICalendarWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 800, 500)
        # self.setFixedSize(1600, 900)
        self.startHubWindow()

    def startHubWindow(self):
        self.HubWindow = UIHubWindow(self)
        self.setWindowTitle("Lotus Home")
        self.setCentralWidget(self.HubWindow)

        ########### Background color ###########
        p = self.HubWindow.palette()
        p.setColor(self.HubWindow.backgroundRole(), QtGui.QColor("#34495e"))
        self.setPalette(p)

        ########### Button handling ###########
        self.HubWindow.new_note_button.clicked.connect(self.startNoteWindow)
        self.HubWindow.scheduled_notes_button.clicked.connect(self.startCalenderWindow)
        self.show()

    def startNoteWindow(self):
        self.NoteWindow = UINoteWindow(self)
        self.setWindowTitle("Lotus Notes")
        self.setCentralWidget(self.NoteWindow)

        ########### Background color ###########
        p = self.NoteWindow.palette()
        p.setColor(self.NoteWindow.backgroundRole(), Qt.white)
        self.setPalette(p)

        ########### Button handling ###########
        self.NoteWindow.go_back_button.clicked.connect(self.startHubWindow)
        self.show()

    def startCalenderWindow(self):
        self.CalenderWindow = UICalendarWindow(self)
        self.setWindowTitle("Scheduled Notes")
        self.setCentralWidget(self.CalenderWindow)

        ########### Background color ###########
        p = self.CalanderWindow.palette()
        p.setColor(self.CalanderWindow.backgroundRole(), Qt.white)
        self.setPalette(p)

        ########### Button handling ###########
        self.CalanderWindow.go_back_button.clicked.connect(self.startHubWindow)
        self.show()

def main():
    wsl.set_display_to_host()
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
