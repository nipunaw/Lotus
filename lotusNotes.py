# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
import sys
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

class UINoteWindow(QWidget):
    def __init__(self, parent=None):
        super(UINoteWindow, self).__init__(parent)

        ########### Writing parameters ###########
        self.pen_utensil = True
        self.eraser_utensil = False
        self.utensil_press = False
        self.brush_size = 3
        self.brush_color = Qt.black
        self.brush_style = Qt.SolidLine
        self.lastPoint = QtCore.QPoint()

        ########### Menu Bar ###########
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("File")
        self.save_option = QtWidgets.QAction("Save", self)
        self.save_option.setShortcut("Ctrl + S")
        self.file_menu.addAction(self.save_option)
        self.save_option.triggered.connect(self.save)

        ########### Canvas color ###########
        self.canvas = QtGui.QPixmap(1600, 900)
        self.canvas.fill(Qt.white)

        ########### Buttons ###########
        self.clear_button_display()
        self.eraser_button_display()
        self.pen_button_display()
        self.go_back_button = QPushButton('Return home', self)
        self.go_back_button.move(50, 50)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.utensil_press = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.utensil_press:
            painter = QtGui.QPainter(self.canvas)
            if self.pen_utensil:
                painter.setPen(QtGui.QPen(self.brush_color, self.brush_size, self.brush_style))
            elif self.eraser_utensil:
                painter.setPen(QtGui.QPen(Qt.white, self.brush_size, self.brush_style))

            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.utensil_press = False
            

    def clear_button_display(self):
        self.clear_button = QtWidgets.QPushButton("Clear All", self)
        self.clear_button.resize(100, 32)
        self.clear_button.move(25, 850)
        self.clear_button.setToolTip("Clear any writing")
        self.clear_button.clicked.connect(self.clear)

    def eraser_button_display(self):
        self.eraser_button = QtWidgets.QPushButton("Eraser", self)
        self.eraser_button.resize(100, 32)
        self.eraser_button.move(150, 850)
        self.eraser_button.setToolTip("Erase any writing")
        self.eraser_button.clicked.connect(self.erase)

    def pen_button_display(self):
        self.pen_button = QtWidgets.QPushButton("Pen", self)
        self.pen_button.setDisabled(self.pen_utensil) # In use by default
        self.pen_button.resize(100, 32)
        self.pen_button.move(275, 850)
        self.pen_button.setToolTip("Premiere writing utensil")
        self.pen_button.clicked.connect(self.pen)

    # Button click handling

    def clear(self):
        # Reset canvas
        self.canvas.fill(Qt.white)
        self.update()
        # Reset back to pen tool
        self.pen()

    def erase(self):
        self.pen_utensil = False
        self.eraser_utensil = True
        self.eraser_button.setDisabled(True)
        self.pen_button.setEnabled(True)

    def pen(self):
        self.pen_utensil = True
        self.eraser_utensil = False
        self.pen_button.setDisabled(True)
        self.eraser_button.setEnabled(True)
            
    def save(self):

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Save Notes", # Caption
                                                             "notes.jpg", # File-name, directory
                                                             "canvass (*.png *.jpg)") # File types
        # Blank file path
        if file_path == "":
            return
        # Saving canvas
        self.canvas.save(file_path)