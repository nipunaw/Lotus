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
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
########### File imports ###########
from lotusHub import UIHubWindow
from lotusNotes import UINoteWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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
            self.HubWindow.new_note_button.clicked.connect(self.NoteWindowSeparate)

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


    def NoteWindowSeparate(self):
        self.newNotes.append(UINoteWindow())
        self.newNotes[self.newNoteCount].setFixedSize(1200, 600)
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
    # def startNoteWindow(self):
    #     self.NoteWindow = UINoteWindow(self)
    #     self.setFixedSize(1200, 600)
    #     self.setWindowTitle("Lotus Notes")
    #     self.setCentralWidget(self.NoteWindow)
    #
    #     ########### Background color ###########
    #     p = self.NoteWindow.palette()
    #     p.setColor(self.NoteWindow.backgroundRole(), Qt.white)
    #     self.setPalette(p)
    #
    #     ########### Button handling ###########
    #     self.NoteWindow.go_back_button.clicked.connect(self.HubWindowSeparate)
    #
    #     self.show()

def main():
    wsl.set_display_to_host()
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()