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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
########### File imports ###########
import configparser
from src.lotusHub import UIHubWindow
from src.lotusNotes import UINoteWindow, set_default_eraser_width, set_default_pen_width
from src.lotusPrevious import UIPreviousWindow
from src.lotusCalender import UICalendarWindow, Schedule
from src.lotusSettings import UISettingsWindow
from src.constants import CONFIG_FILE, SCHEDULED_NOTES_DIRECTORY
########### Other imports ###########
import os

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.default_config()
        self.schedule = Schedule()
        self.schedule.connect_buttons.connect(self.connect_scheduled_notes_buttons)
        self.first_time = True
        self.newNoteCount = 0
        self.newNotes = []
        self.initUI()
        self.HubWindowSeparate()

        ###### Attempting to center (experimental) ######

    def default_config(self):
        os.makedirs(SCHEDULED_NOTES_DIRECTORY, exist_ok=True)
        try:
            file = open(CONFIG_FILE, 'r')
        except IOError:
            file = open(CONFIG_FILE, 'w')
            config = configparser.ConfigParser()
            config['DEFAULT'] = {'Name': '',
                                 'Pen_Size': '5',
                                 'Eraser_Size': '5',
                                 'Name_Heading': 'True'}
            config.write(file)
        file.close()

    def initUI(self):
        screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())
        fg = self.frameGeometry()
        fg.moveCenter(screen.geometry().center())
        self.move(fg.topLeft())

    def HubWindowSeparate(self):
        if self.first_time:
            self.first_time = False
            self.HubWindow = UIHubWindow(self.schedule)
            self.HubWindow.setFixedSize(800, 500)
            self.HubWindow.setWindowTitle("Lotus Home")

            ########### Background color ###########
            p = self.HubWindow.palette()
            p.setColor(self.HubWindow.backgroundRole(), QtGui.QColor(Qt.white))
            self.HubWindow.setPalette(p)

            ########### Button handling ###########
            self.HubWindow.new_note_button.clicked.connect(lambda: self.NoteWindowSeparate(None))
            self.HubWindow.schedule_button.clicked.connect(
                lambda state, x=self.schedule: self.startCalenderWindow(self.schedule))
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


    def NoteWindowSeparate(self, file_path=None, scheduled=False, event_name=None, event_date=None, event_time=None):
        window = UINoteWindow(file_path=file_path, scheduled=scheduled)
        self.newNotes.append(window)
        if file_path:
            if scheduled:
                if not os.path.isfile(file_path):
                    file_name = "{}-{}.jpg".format(event_name, event_time.toString("HHmmAP"))
                    os.makedirs(file_path.replace(file_name, ""), exist_ok=True)
                window_title = "{} - {} - {} - Scheduled Notes".format(event_name, event_date.toString("MM/dd/yyyy"), event_time.toString("HH:mm AP"))
                self.newNotes[self.newNoteCount].setWindowTitle(window_title)
            else:
                window.deleted_file.connect(self.PreviousWindow.delete_button)
                self.newNotes[self.newNoteCount].setWindowTitle(file_path)
        else:
            self.newNotes[self.newNoteCount].setWindowTitle("New Note " + str(self.newNoteCount + 1))
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
        self.PreviousWindow = UIPreviousWindow(set_paths=False)
        self.PreviousWindow.setFixedSize(600, 400)
        self.PreviousWindow.setMaximumSize(600, 400) # not working
        self.setWindowTitle("Previous Notes")
        self.setCentralWidget(self.PreviousWindow)

        ########### Background color ###########
        p = self.PreviousWindow.palette()
        p.setColor(self.PreviousWindow.backgroundRole(), Qt.white)
        self.setPalette(p)

        ########### Button handling ###########
        for i in range(len(self.PreviousWindow.directories)):
             try:
                 # self.PreviousWindow.buttons[self.PreviousWindow.directories[i]].clicked.connect(
                 #     lambda state, x=self.PreviousWindow.directories[i]: self.NoteWindowSeparate(x))
                 self.PreviousWindow.buttons[self.PreviousWindow.directories[i]].clicked.connect(
                     lambda state, x=self.PreviousWindow.directories[i]: self.NoteWindowSeparate(file_path=x))
                 self.PreviousWindow.other_buttons[self.PreviousWindow.directories[i]].clicked.connect(
                        lambda state, x=self.PreviousWindow.directories[i]: self.NoteWindowSeparate(x))
             except KeyError:
                pass

        self.show()

    def connect_scheduled_notes_buttons(self, buttons: list):
        for (button, name, date, time) in buttons:
            file_name = "{}-{}.jpg".format(name, time.toString("HHmmAP"))
            file_path = SCHEDULED_NOTES_DIRECTORY + "{}/{}/{}/{}".format(date.year(), date.month(), date.day(),
                                                                         file_name)
            button.clicked.connect(
                lambda state, w=file_path, x=name, y=date, z=time: self.NoteWindowSeparate(scheduled=True, file_path=w,
                                                                                           event_name=x, event_date=y,
                                                                                           event_time=z))

    def update_header(self, name):
        self.HubWindow.user_welcome.setText("Welcome back "+ name)

    def startSettingsWindow(self):
        self.SettingsWindow = UISettingsWindow()
        self.SettingsWindow.pen_width_updated.connect(set_default_pen_width)
        self.SettingsWindow.eraser_width_updated.connect(set_default_eraser_width)
        self.SettingsWindow.name_updated.connect(self.update_header) # lambda state, x = self.updateSettingsWindow() : self.HubWindow.user_welcome.setText(x)
        self.setWindowTitle("Settings")
        self.setCentralWidget(self.SettingsWindow)

        ########### Background color ###########
        p = self.SettingsWindow.palette()
        p.setColor(self.SettingsWindow.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.show()

    def connectCalendarWindowButtons(self, buttons : list):
        for (button, cls, date) in buttons:
            file_path = SCHEDULED_NOTES_DIRECTORY + "{}/{}/{}/{}.jpg".format(date.year(), date.month(), date.day(), cls["name"])
            if not os.path.isfile(file_path):
                os.makedirs(file_path.replace("/{}.jpg".format(cls["name"]), ""), exist_ok=True)
            button.clicked.connect(lambda state, x=file_path, y=cls, z=date: self.NoteWindowSeparate(x, scheduled=True, cls=y, date=z))

    def startCalenderWindow(self, schedule: Schedule):
        self.CalenderWindow = UICalendarWindow(schedule, parent=self)
        self.setWindowTitle("Scheduled Notes")
        self.setCentralWidget(self.CalenderWindow)
        self.show()

def main():
    src.wsl.set_display_to_host()
    app = QApplication(sys.argv)
    os.makedirs(SCHEDULED_NOTES_DIRECTORY, exist_ok=True)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
