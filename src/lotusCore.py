# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### WSL import ###########
import src.wsl
########### PyQT5 imports ###########
import sys
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
########### File imports ###########
import configparser
from src.lotusHub import UIHubWindow
from src.lotusNotes import UINoteWindow
from src.lotusPrevious import UIPreviousWindow
from src.lotusCalender import UICalendarWindow
########### Other imports ###########
import os

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/config.ini')
SCHEDULE_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/schedule.json')
SCHEDULED_NOTES_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname( __file__ )), 'data/')

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        try:
            file = open(CONFIG_FILE, 'r')
        except IOError:
            file = open(CONFIG_FILE, 'w')
            config = configparser.ConfigParser()
            config['DEFAULT'] = {'Name': ''}
            config.write(file)
        file.close()
        self.first_time = True
        self.newNoteCount = 0
        self.newNotes = []
        self.initUI()
        self.HubWindowSeparate()

        ###### Attempting to center (experimental) ######
    def initUI(self):
        screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())
        fg = self.frameGeometry()
        fg.moveCenter(screen.geometry().center())
        self.move(fg.topLeft())

    def HubWindowSeparate(self):
        if self.first_time:
            self.first_time = False
            self.HubWindow = UIHubWindow()
            self.HubWindow.setFixedSize(800, 500)
            self.HubWindow.setWindowTitle("Lotus Home")

            ########### Background color ###########
            p = self.HubWindow.palette()
            p.setColor(self.HubWindow.backgroundRole(), QtGui.QColor(Qt.white))
            self.HubWindow.setPalette(p)

            ########### Button handling ###########
            self.HubWindow.new_note_button.clicked.connect(lambda: self.NoteWindowSeparate(None))
            self.HubWindow.schedule_button.clicked.connect(self.startCalenderWindow)
            self.HubWindow.previous_notes_button.clicked.connect(self.startPreviousWindow)

            self.HubWindow.show()

        elif self.HubWindow.isHidden():
            self.HubWindow.setHidden(False)
        else:
            self.HubWindow.setHidden(True)

            # Switching focus doesn't work well in X11 apps

            #print("Should switch focus")
            #self.HubWindow.showNormal()
            #self.HubWindow.raise_()
            #self.HubWindow.activateWindow()
            #self.HubWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
            #print(self.HubWindow.isActiveWindow())
            #self.HubWindow.setWindowFlags(self.HubWindow.windowFlags() & QtCore.Qt.WindowStaysOnTopHint)  # set always on top flag, makes window disappear
            #self.HubWindow.update() # makes window reappear, but it's ALWAYS on top
            #self.HubWindow.setWindowFlags(self.HubWindow.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)  # clear always on top flag, makes window disappear
            #self.HubWindow.update()
            #self.HubWindow.setFocus(True)
            #self.HubWindow.setWindowState(self.HubWindow.windowState() & QtCore.Qt.WindowActive)
            #self.activateWindow()
            #self.raise_()


    def NoteWindowSeparate(self, directory, scheduled=False, cls=None, date=None):
        window = UINoteWindow(directory, scheduled=scheduled)
        self.newNotes.append(window)
        self.newNotes[self.newNoteCount].setFixedSize(1200, 600)
        if directory:
            if scheduled and cls is not None:
                cls_title = "{} - {} - Scheduled Notes".format(cls["name"], date.toString("MM/dd/yyyy"), cls)
                self.newNotes[self.newNoteCount].setWindowTitle(cls_title)
            else:
                window.deleted_file.connect(self.PreviousWindow.delete_button)
                self.newNotes[self.newNoteCount].setWindowTitle(directory)
        else:
            self.newNotes[self.newNoteCount].setWindowTitle("New Note " + str(self.newNoteCount + 1) if directory is None else directory)
        self.newNotes[self.newNoteCount].home_button.clicked.connect(self.HubWindowSeparate)
        self.newNotes[self.newNoteCount].show()
        self.newNoteCount += 1

    # def startHubWindow(self):
    #     self.HubWindow = UIHubWindow(self)
    #     self.setFixedSize(800, 500)
    #     self.setWindowTitle("Lotus Home")
    #     self.setCentralWidget(self.HubWindow)
    #
    #     ########### Background color ###########
    #     p = self.HubWindow.palette()
    #     p.setColor(self.HubWindow.backgroundRole(), QtGui.QColor(Qt.white))
    #     self.setPalette(p)
    #
    #     ########### Button handling ###########
    #     self.HubWindow.new_note_button.clicked.connect(self.NoteWindowSeparate)
    #     self.show()
    #

    # def startNoteWindow(self, directory):
    #     if directory is not None:
    #         directory = directory[:-1]
    #     self.NoteWindow = UINoteWindow(self, directory)
    #     self.setWindowTitle("Lotus Notes")
    #     self.setCentralWidget(self.NoteWindow)
    #
    #     ########### Background color ###########
    #     p = self.NoteWindow.palette()
    #     p.setColor(self.NoteWindow.backgroundRole(), Qt.white)
    #     self.setPalette(p)
    #
    #     ########### Button handling ###########
    #     self.NoteWindow.go_back_button.clicked.connect(self.startHubWindow)
    #     self.show()

    def startPreviousWindow(self):
        self.PreviousWindow = UIPreviousWindow(self)
        self.setWindowTitle("Non-Scheduled Notes")
        self.setCentralWidget(self.PreviousWindow)

        ########### Background color ###########
        p = self.PreviousWindow.palette()
        p.setColor(self.PreviousWindow.backgroundRole(), Qt.white)
        self.setPalette(p)

        ########### Button handling ###########
        for i in range(len(self.PreviousWindow.directories)):
            self.PreviousWindow.buttons[self.PreviousWindow.directories[i]].clicked.connect(lambda state, x=self.PreviousWindow.directories[i]: self.NoteWindowSeparate(x))

        self.show()

    def connectCalendarWindowButtons(self, buttons : list):
        for (button, cls, date) in buttons:
            file_path = SCHEDULED_NOTES_DIRECTORY + "{}/{}/{}/{}.jpg".format(date.year(), date.month(), date.day(), cls["name"])
            if not os.path.isfile(file_path):
                os.makedirs(file_path.replace("/{}.jpg".format(cls["name"]), ""), exist_ok=True)
            button.clicked.connect(lambda state, x=file_path, y=cls, z=date: self.NoteWindowSeparate(x, scheduled=True, cls=y, date=z))

    def startCalenderWindow(self):
        self.CalenderWindow = UICalendarWindow(parent=self)
        self.setWindowTitle("Scheduled Notes")
        self.setCentralWidget(self.CalenderWindow)
        self.CalenderWindow.calendarWidget.buttonsUpdated.connect(self.connectCalendarWindowButtons)
        ########### Button handling ###########
        # self.CalanderWindow.go_back_button.clicked.connect(self.startHubWindow)
        self.show()

def main():
    src.wsl.set_display_to_host()
    app = QApplication(sys.argv)
    os.makedirs(SCHEDULED_NOTES_DIRECTORY, exist_ok=True)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
