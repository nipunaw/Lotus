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

DIRECTORY_FILE = "../data/directories.txt"

class UINoteWindow(QWidget):
    def __init__(self, directory, parent=None):
        super(UINoteWindow, self).__init__(parent)

        self.directory = directory

        ########### Writing parameters ###########
        # General utensil parameters
        self.pen_utensil = True
        self.eraser_utensil = False
        self.utensil_press = False
        # Pen default parameters
        self.pen_current = QtGui.QPen()
        self.pen_brush_size = 4
        self.pen_brush_color = Qt.black
        self.pen_brush_style = Qt.SolidLine
        self.pen_cap_style = Qt.RoundCap
        self.pen_join_style = Qt.RoundJoin
        self.pen_lastPoint = QtCore.QPoint()
        self.pen_init_update()
        # Eraser default parameters
        self.eraser_current = QtGui.QPen()
        self.eraser_brush_size = 4
        self.eraser_brush_color = Qt.white
        self.eraser_brush_style = Qt.SolidLine
        self.eraser_cap_style = Qt.RoundCap
        self.eraser_join_style = Qt.RoundJoin
        self.eraser_lastPoint = QtCore.QPoint()
        self.eraser_init_update()

        ########### Menu Bar ###########
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("File")
        self.template_menu = self.menu_bar.addMenu("Template")
        self.save_option = QtWidgets.QAction("Save", self)
        self.save_option.setShortcut("Ctrl+S")
        self.save_as_option = QtWidgets.QAction("Save As", self)
        self.save_as_option.setShortcut("F12")
        self.heading_option = QtWidgets.QAction("Add Heading", self)
        self.heading_option.setShortcut("Ctrl+H")
        self.file_menu.addAction(self.save_option)
        self.file_menu.addAction(self.save_as_option)
        self.template_menu.addAction(self.heading_option)
        self.save_option.triggered.connect(self.save)
        self.save_as_option.triggered.connect(self.save_as)
        self.heading_option.triggered.connect(self.heading)
        self.open_option = QtWidgets.QAction("Open", self)
        self.file_menu.addAction(self.open_option)
        self.open_option.triggered.connect(self.open)


        ########### Canvas color ###########
        # Handled by resizeEvent
        self.first_time = True

        ########### Saving ###########
        self.file_path = ""

        ########### Closing ###########
        self.new_strokes_since_save = False

        ########### Buttons ###########
        # Handled by resizeEvent
        self.home_button = QPushButton('Toggle home', self)

    ########### Utensil initialization/updates ###########
    def pen_init_update(self):
        self.pen_current.setStyle(self.pen_brush_style)
        self.pen_current.setWidth(self.pen_brush_size)
        self.pen_current.setBrush(self.pen_brush_color)
        self.pen_current.setCapStyle(self.pen_cap_style)
        self.pen_current.setJoinStyle(self.pen_join_style)

    def eraser_init_update(self):
        self.eraser_current.setStyle(self.eraser_brush_style)
        self.eraser_current.setWidth(self.eraser_brush_size)
        self.eraser_current.setBrush(self.eraser_brush_color)
        self.eraser_current.setCapStyle(self.eraser_cap_style)
        self.eraser_current.setJoinStyle(self.eraser_join_style)

    ########### Closing ###########

    def closeEvent(self, event):
        compare_canvas = QtGui.QPixmap(self.size().width(), self.size().height())
        compare_canvas.fill(Qt.white)
        compare_canvas_image = compare_canvas.toImage()
        current_canvas_image = self.canvas.toImage()
        if not current_canvas_image == compare_canvas_image:
            if self.new_strokes_since_save:
                self.savePopup()

    def savePopup(self):
        save_prompt = QtWidgets.QDialog(self)
        save_prompt.setWindowTitle("Save your changes?")
        options = QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        save_prompt.buttonBox = QtWidgets.QDialogButtonBox(options)
        save_prompt.buttonBox.accepted.connect(self.acceptSave)
        save_prompt.buttonBox.rejected.connect(save_prompt.reject)
        save_prompt.layout = QtWidgets.QVBoxLayout()
        save_prompt.layout.addWidget(save_prompt.buttonBox)
        save_prompt.setLayout(save_prompt.layout)
        save_prompt.exec_()

    def acceptSave(self):
        self.save()
        self.deleteLater()

    ########### Resizing ###########

    def resizeEvent(self, event):
        if self.first_time:
            self.canvas = QtGui.QPixmap(self.size().width(), self.size().height())
            self.canvas.fill(Qt.white)
            self.home_button_display()
            self.clear_button_display()
            self.eraser_button_display()
            self.pen_button_display()
            self.first_time = False
            if self.directory is not None:
                self.open_directory(self.directory)
        else: # Not reached
            newCanvas = self.canvas.scaled(self.size().width(), self.size().height())
            self.canvas = newCanvas


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.utensil_press = True
            painter = QtGui.QPainter(self.canvas)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            if self.pen_utensil:
                self.new_strokes_since_save = True
                painter.setPen(QtGui.QPen(self.pen_current))
            elif self.eraser_utensil:
                painter.setPen(QtGui.QPen(self.eraser_current))
            painter.drawPoint(event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.utensil_press:
            painter = QtGui.QPainter(self.canvas)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            if self.pen_utensil:
                painter.setPen(QtGui.QPen(self.pen_current))
            elif self.eraser_utensil:
                painter.setPen(QtGui.QPen(self.eraser_current))

            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.utensil_press = False
            

    def home_button_display(self):
        #self.home_button.setEnabled(False)
        self.home_button.resize(100, 32)
        self.home_button.move(self.size().width()-125, self.size().height() - 50)
        self.home_button.setToolTip("Clear any writing")

    def clear_button_display(self):
        self.clear_button = QtWidgets.QPushButton("Clear All", self)
        self.clear_button.resize(100, 32)
        self.clear_button.move(25, self.size().height()-50)
        self.clear_button.setToolTip("Clear any writing")
        self.clear_button.clicked.connect(self.clear)

    def eraser_button_display(self):
        self.eraser_button = QtWidgets.QPushButton("Eraser", self)
        self.eraser_button.resize(100, 32)
        self.eraser_button.move(150, self.size().height()-50)
        self.eraser_button.setToolTip("Erase any writing")
        self.eraser_button.clicked.connect(self.erase)

    def pen_button_display(self):
        self.pen_button = QtWidgets.QPushButton("Pen", self)
        self.pen_button.setDisabled(self.pen_utensil) # In use by default
        self.pen_button.resize(100, 32)
        self.pen_button.move(275, self.size().height()-50)
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

    ########### Saving ###########

    def save(self):
        if self.file_path == "":
            self.save_as()
        else:
            self.new_strokes_since_save = False
            self.canvas.save(self.file_path)

    def save_as(self):
        self.file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "Save Notes", # Caption
                                                             "notes.jpg", # File-name, directory
                                                             "JPG (*.jpg);;PNG (*.png)") # File types

        with open(DIRECTORY_FILE, "a") as f:
            f.write(self.file_path + "\n")
        count = 0
        for line in open(DIRECTORY_FILE):
            count += 1
        if count == 7:
            with open(DIRECTORY_FILE) as fin:
                data = fin.read().splitlines(True)
            with open(DIRECTORY_FILE, 'w') as fout:
                fout.writelines(data[1:])

        # Blank file path
        if self.file_path == "":
            return
        self.new_strokes_since_save = False
        # Saving canvas
        self.canvas.save(self.file_path)
        self.setWindowTitle(self.file_path)

    def heading(self):
        painter = QtGui.QPainter(self.canvas)
        arial_font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        painter.setFont(arial_font)
        painter.drawText(10, 50, "Carlos Morales-Diaz")
        painter.drawText(10, 75, "October 14, 2020")
        painter.drawText(10, 100, "CIS4930")
        self.update()
    def open(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/home", "JPG (*.jpg);;PNG (*.png)")
        self.open_directory(file_path)

    def open_directory(self, file_path):
        self.canvas = QtGui.QPixmap(file_path)
        newCanvas = self.canvas.scaled(self.size().width(), self.size().height())
        self.canvas = newCanvas
        self.update()
