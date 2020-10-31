# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

import configparser
import json
########### PyQT5 imports ###########
import os
from datetime import date
from enum import Enum

import pytesseract
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPoint, QRect
from PyQt5.QtGui import QRegion, QColor
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QMessageBox, QScrollArea, QGridLayout, QHBoxLayout, \
    QVBoxLayout, QSizePolicy

from src.constants import CONFIG_FILE, DIRECTORY_FILE, SCHEDULE_FILE_PATH

class Utensil:
    def __init__(self, color : QColor, radius : int,
                 brush_style : Qt.PenStyle = Qt.SolidLine,
                 cap_style : Qt.PenCapStyle = Qt.RoundCap,
                 join_style : Qt.PenJoinStyle = Qt.RoundJoin):
        self.maxWidth = 50
        self.color = color
        self.radius = radius
        self.brush_style = brush_style
        self.cap_style = cap_style
        self.join_style = join_style

    def incrementWidth(self):
        result = self.radius + 1
        self.radius = result if result < self.maxWidth else self.maxWidth

    def decrementWidth(self):
        result = self.radius - 1
        self.radius = result if result >= 1 else 1

    def pen(self):
        pen = QtGui.QPen()
        pen.setStyle(self.brush_style)
        pen.setWidth(self.radius)
        pen.setColor(self.color)
        pen.setCapStyle(self.cap_style)
        pen.setJoinStyle(self.join_style)
        return pen

class Utensils(Utensil, Enum):
    PEN = (Qt.black, 4)
    ERASER = (Qt.white, 4)

class Canvas(QLabel):
    scrolled = pyqtSignal(QtGui.QWheelEvent)
    mouse_grab = pyqtSignal(QPoint)
    def __init__(self):
        super(Canvas, self).__init__()
        self.setStyleSheet("background-color: black")
        self.canvas = QtGui.QPixmap(self.size())
        self.canvas.fill(Qt.white)
        self.setPixmap(self.canvas)
        self.last_save = None
        ########### Writing parameters ###########
        # General utensil parameters
        self.utensil_press = False
        self.current_utensil = Utensils.PEN
        # Scrolling Parameters
        self.mouse_button_scrolling = False
        # Pen default parameters
        self.pen_lastPoint = QtCore.QPoint()
        # Eraser default parameters
        self.eraser_lastPoint = QtCore.QPoint()
        self.cursor = QtGui.QCursor()
        self.cursor.setShape(Qt.CrossCursor)
        self.setCursor(self.cursor)

    def resizeCanvas(self, size):
        temp = self.canvas
        self.canvas = QtGui.QPixmap(size)
        self.canvas.fill(Qt.white)
        painter = QtGui.QPainter(self.canvas)
        painter.drawPixmap(temp.rect(), temp, temp.rect())
        self.setPixmap(self.canvas)
        if self.last_save is None:
            self.last_save = self.canvas
            self.hasChanged()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if self.canvas.size() != self.size():
            self.resizeCanvas(self.size())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.utensil_press = True
            painter = QtGui.QPainter(self.canvas)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(self.current_utensil.pen())
            painter.drawPoint(event.pos())
            self.last_point_draw = event.pos()
            self.update()
            painter.end()
        elif event.button() == Qt.MiddleButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.last_point_scroll = event.globalPos()
            self.mouse_button_scrolling = True
        else:
            super(Canvas, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() and Qt.LeftButton and self.utensil_press:
            if self.width() - event.pos().x() < 20:
                self.resizeCanvas(QSize(self.width() + 100, self.height()))
            if self.height() - event.pos().y() < 20:
                self.resizeCanvas(QSize(self.width(), self.height() + 100))
            painter = QtGui.QPainter(self.canvas)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(self.current_utensil.pen())
            painter.drawLine(self.last_point_draw, event.pos())
            self.last_point_draw = event.pos()
            self.update()
            painter.end()
        elif event.buttons() and Qt.MiddleButton and self.mouse_button_scrolling:
            offset = self.last_point_scroll - event.globalPos()
            self.last_point_scroll = event.globalPos()
            self.mouse_grab.emit(offset)
        else:
            super(Canvas, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.utensil_press = False
        elif event.button() == Qt.MiddleButton:
            self.setCursor(self.cursor)
            self.mouse_button_scrolling = False

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.scrolled.emit(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.canvas)
        painter.end()
        self.hasChanged()

    def hasChanged(self):
        if self.last_save is None:
            return False
        return not self.pixmap().toImage() == self.last_save.toImage()

    def save(self, file_path):
        self.canvas.save(file_path)
        self.last_save = self.canvas

    def setUtensil(self, utensil : Utensil):
        self.current_utensil = utensil

    # Button click handling
    def clear(self):
        # Reset canvas
        self.canvas.fill(Qt.white)
        self.resizeCanvas(self.minimumSize())
        self.update()
        # Reset back to pen tool
        self.setUtensil(Utensils.PEN)

    def loadImage(self, file_path):
        image_pixmap = QtGui.QPixmap(file_path)
        canvas = QtGui.QPixmap(self.minimumSize().expandedTo(image_pixmap.size()))
        painter = QtGui.QPainter(canvas)
        painter.drawPixmap(canvas.rect(), image_pixmap, image_pixmap.rect())
        self.canvas = canvas
        self.setPixmap(canvas)
        self.last_save = self.canvas

class CanvasWindow(QScrollArea):
    def __init__(self):
        super(CanvasWindow, self).__init__()
        self.setWidgetResizable(True)
        self.layout = QVBoxLayout()
        self.label = Canvas()
        self.label.setMinimumSize(self.layout.minimumSize())
        self.label.scrolled.connect(self.scrollForLabel)
        self.label.mouse_grab.connect(self.mouseGrabScroll)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.label, Qt.AlignTop | Qt.AlignLeft)

        self.setWidget(self.label)
        self.setLayout(self.layout)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def mouseGrabScroll(self, offset):
        x = self.horizontalScrollBar().value() + offset.x()
        y = self.verticalScrollBar().value() + offset.y()
        self.horizontalScrollBar().setValue(x)
        self.verticalScrollBar().setValue(y)

    def scrollForLabel(self, event: QtGui.QWheelEvent):
        hval = self.horizontalScrollBar().value()
        vval = self.verticalScrollBar().value()
        newx = hval - (event.angleDelta().x() / (8 * 15)) * self.horizontalScrollBar().singleStep()
        newy = vval - (event.angleDelta().y() / (8 * 15)) * self.verticalScrollBar().singleStep()
        hmin = self.horizontalScrollBar().minimum()
        hmax = self.horizontalScrollBar().maximum()
        if hmin < newx < hmax:
            self.horizontalScrollBar().setValue(newx)
        elif hmin >= newx:
            self.horizontalScrollBar().setValue(hmin)
        elif hmax <= newx:
            self.horizontalScrollBar().setValue(hmax)
        ymin = self.verticalScrollBar().minimum()
        ymax = self.verticalScrollBar().maximum()
        if ymin < newy < ymax:
            self.verticalScrollBar().setValue(newy)
        elif ymin >= newy:
            self.verticalScrollBar().setValue(ymin)
        elif ymax <= newy:
            self.verticalScrollBar().setValue(ymax)

class UINoteWindow(QWidget):
    deleted_file = pyqtSignal(str)

    def __init__(self, directory : str, parent=None, scheduled=False):
        super(UINoteWindow, self).__init__(parent)

        self.directory = directory
        self.scheduled = scheduled

        ########### Menu Bar ###########
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("File")
        self.template_menu = self.menu_bar.addMenu("Template")
        self.settings_menu = self.menu_bar.addMenu("Settings")
        self.save_option = QtWidgets.QAction("Save", self)
        self.save_option.setShortcut("Ctrl+S")
        self.save_as_option = QtWidgets.QAction("Save As" if not scheduled else "Export", self)
        self.save_as_option.setShortcut("F12")
        self.heading_option = QtWidgets.QAction("Add/Edit Heading", self)
        self.heading_option.setShortcut("Ctrl+H")
        self.settings_option = QtWidgets.QAction("Font")
        self.settings_menu.addAction(self.settings_option)
        self.file_menu.addAction(self.save_option)
        self.file_menu.addAction(self.save_as_option)
        self.template_menu.addAction(self.heading_option)
        self.save_option.triggered.connect(self.save)
        self.save_as_option.triggered.connect(self.save_as)
        self.heading_option.triggered.connect(self.heading)
        self.settings_option.triggered.connect(self.settings)
        self.open_option = QtWidgets.QAction("Open", self)
        self.open_option.setShortcut("Ctrl+O")
        self.file_menu.addAction(self.open_option)
        self.open_option.triggered.connect(self.open)
        self.ocr_menu = self.menu_bar.addMenu("OCR")
        self.find_ocr = QtWidgets.QAction("Find Typed/Neat Text", self)
        self.ocr_menu.addAction(self.find_ocr)
        self.find_ocr.triggered.connect(self.ocr)

        ########### Buttons ###########
        # Handled by resizeEvent
        self.home_button = QPushButton('Toggle home', self)
        self.font = QtGui.QFont("Times New Roman", 20, QtGui.QFont.Bold)
        self.title = QtWidgets.QLineEdit()
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        name = config['DEFAULT']['name']
        self.name = QtWidgets.QLineEdit(name)
        self.course = QtWidgets.QComboBox()
        self.add_date = True

        ########### Layout ############
        self.setMinimumSize(1200, 600)
        self.canvas_window = CanvasWindow()
        self.canvas_window.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layout = QVBoxLayout()
        # heading = QtWidgets.QLineEdit()
        # heading.setStyleSheet("border: 0px")
        # self.layout.addWidget(heading)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.canvas_window, Qt.AlignTop)
        self.button_layout = QGridLayout()
        self.button_layout.setContentsMargins(10,10,10,10)

        self.home_button_display()
        self.clear_button_display()
        self.eraser_button_display()
        self.pen_button_display()

        self.layout.addLayout(self.button_layout, Qt.AlignBottom)
        self.setLayout(self.layout)
        self.layout.setMenuBar(self.menu_bar)

        ########### Saving/Opening ###########
        if self.scheduled:
            self.file_path = self.directory
            self.open_directory(self.file_path)
        elif self.directory is not None:
            self.file_path = self.directory[:-1]
            self.open_directory(self.file_path)
        else:
            self.file_path = ""

        self.file_path_2 = ""

    ########### Closing ###########
    def closeEvent(self, event):
        if self.canvas_window.label.hasChanged():
            self.savePopup()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_BracketLeft:
            for u in Utensils:
                u.decrementWidth()
        elif event.key() == Qt.Key_BracketRight:
            for u in Utensils:
                u.incrementWidth()

    def savePopup(self):
        self.save_prompt = QtWidgets.QDialog(self)
        self.save_prompt.setWindowTitle("Save your changes?")
        options = QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        self.save_prompt.buttonBox = QtWidgets.QDialogButtonBox(options)
        self.save_prompt.buttonBox.accepted.connect(self.acceptSave)
        self.save_prompt.buttonBox.rejected.connect(self.save_prompt.reject)
        self.save_prompt.layout = QtWidgets.QVBoxLayout()
        self.save_prompt.layout.addWidget(self.save_prompt.buttonBox)
        self.save_prompt.setLayout(self.save_prompt.layout)
        self.save_prompt.exec_()

    def acceptSave(self):
        self.save()
        self.save_prompt.deleteLater()

    def erase(self):
        self.canvas_window.label.setUtensil(Utensils.ERASER)
        self.eraser_button.setDisabled(True)
        self.pen_button.setEnabled(True)

    def pen(self):
        self.canvas_window.label.setUtensil(Utensils.PEN)
        self.pen_button.setDisabled(True)
        self.eraser_button.setEnabled(True)

    def home_button_display(self):
        self.button_layout.addWidget(self.home_button, 0, 3)
        self.home_button.setToolTip("Clear any writing")

    def clear_button_display(self):
        self.clear_button = QtWidgets.QPushButton("Clear All", self)
        self.button_layout.addWidget(self.clear_button, 0, 2)
        self.clear_button.setToolTip("Clear any writing")
        self.clear_button.clicked.connect(self.canvas_window.label.clear)

    def eraser_button_display(self):
        self.eraser_button = QtWidgets.QPushButton("Eraser", self)
        self.button_layout.addWidget(self.eraser_button, 0, 1)
        self.eraser_button.setToolTip("Erase any writing")
        self.eraser_button.clicked.connect(self.erase)

    def pen_button_display(self):
        self.pen_button = QtWidgets.QPushButton("Pen", self)
        self.pen_button.setDisabled(False) # In use by default
        self.pen_button.resize(100, 32)
        self.button_layout.addWidget(self.pen_button, 0, 0)
        self.pen_button.setToolTip("Premiere writing utensil")
        self.pen_button.clicked.connect(self.pen)


    ########### Saving ###########
    def save(self):
        if self.file_path == "":
            self.save_as()
        else:
            self.canvas_window.label.save(self.file_path)

    def save_as(self):
        self.file_path_2, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                    "Save Notes", # Caption
                                                                    "notes.jpg", # File-name, directory
                                                                    "JPG (*.jpg);;PNG (*.png)") # File types

        # Blank file path
        if self.file_path_2 == "":
            return
        self.file_path =  self.file_path_2
        try:
            #file exists
            with open(DIRECTORY_FILE, "r") as f:
                paths = f.read().splitlines()
            count = len(paths)
            if self.file_path in paths:
                paths.remove(self.file_path)
                paths.append(self.file_path)
                with open(DIRECTORY_FILE, "w") as f:
                    f.writelines(p + "\n" for p in paths)
            elif count == 7 or (count > 7 and paths[8] == ""):
                with open(DIRECTORY_FILE, "w") as f:
                    paths = paths[0:6]
                    paths.append(self.file_path)
                    f.writelines(p + "\n" for p in paths)
            elif count < 7:
                with open(DIRECTORY_FILE, "a") as f:
                    f.writelines([self.file_path + "\n"])
        except Exception as e:
            with open(DIRECTORY_FILE, "w+") as f:
                f.write(self.file_path + "\n")

        # Saving canvas
        self.canvas_window.label.save(self.file_path)
        self.setWindowTitle(self.file_path)

    ########### Heading ###########
    def heading(self):
        try:
            with open(SCHEDULE_FILE_PATH) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        name_classes = []
        for b in data:
            name_classes.append(b['name'])
        header_dialog = QtWidgets.QDialog(self)
        header_dialog.setWindowTitle("Add a header")
        layout = QtWidgets.QFormLayout()
        title_edit = QtWidgets.QLineEdit()
        name_edit = QtWidgets.QLineEdit()
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        name = config['DEFAULT']['name']
        name_edit.setText(name)
        if self.name.text() != name:
            name_edit.setText(self.name.text())
        title_edit.setText(self.title.text())
        layout.addRow(self.tr("&Title:"), title_edit, )
        layout.addRow(self.tr("&Name:"), name_edit)
        time_checkbox = QtWidgets.QCheckBox("Add Date", self)
        time_checkbox.setChecked(self.add_date)
        dropdown = QtWidgets.QComboBox(self)
        for classes in name_classes:
            dropdown.addItem(classes)
        dropdown.addItem("---")
        dropdown.setCurrentText(self.course.currentText())
        layout.addWidget(time_checkbox)
        layout.addRow(dropdown)
        self.title = title_edit
        self.name = name_edit

        add_button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        add_button.accepted.connect(
            lambda: self.accept_header(self.title, self.name, dropdown, time_checkbox, header_dialog))
        add_button.rejected.connect(header_dialog.close)
        add_button.setOrientation(Qt.Horizontal)
        layout.addWidget(add_button)
        header_dialog.setLayout(layout)
        header_dialog.update()
        header_dialog.show()
        self.update()

    def accept_header(self, title, name, course, time_checkbox, dialog):

        if len(title.text()) == 0 and len(name.text()) == 0 and course.currentText() == "---" and (not time_checkbox.isChecked()):
            #prompt to add at least one field
            error = QtWidgets.QMessageBox()
            error.setText("Please fill out at least one entry.")
            error.exec_()
            return

        today = date.today()
        # time = datetime.now()
        date_str = today.strftime("%B %d, %Y")
        # time_str = time.strftime("%H:%M:%S")
        painter = QtGui.QPainter(self.canvas_window.label.canvas)
        rect = QtCore.QRect(8, 20, 750, 150)
        painter.fillRect(rect, Qt.white)
        painter.setFont(self.font)
        font_size = self.font.pointSize()
        x = 0
        if len(title.text()) != 0:
            painter.drawText(10, 30 + font_size, title.text())
        else:
            x = -25
        if len(name.text()) != 0:
            painter.drawText(10, 55 + font_size + x, name.text())
        else:
            x = x - 25
        painter.setPen(Qt.black)
        self.add_date = time_checkbox.isChecked()
        if self.add_date:
            painter.drawText(10, 80 + font_size + x, date_str)
        else:
            x = x - 25
        self.course = course
        if course.currentText() != "---":
            painter.drawText(10, 105 + font_size + x, course.currentText())
        dialog.close()
        self.update()
        return

    def settings(self):
        arial_font = QtGui.QFont("Times New Roman", 20, QtGui.QFont.Bold)
        font, ok = QtWidgets.QFontDialog.getFont(arial_font)
        if ok:
            self.font = font
        dialog = QtWidgets.QDialog()
        time_checkbox = QtWidgets.QCheckBox("", self)
        time_checkbox.setChecked(self.add_date)
        self.accept_header(self.title, self.name, self.course, time_checkbox, dialog)

    def open(self):
        if self.canvas_window.label.hasChanged():
            self.savePopup()
        self.file_path_2, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/home", "JPG (*.jpg);;PNG (*.png)")
        if self.file_path_2 == "":
            return
        self.file_path = self.file_path_2
        self.open_directory(self.file_path)
        self.setWindowTitle(self.file_path)

    def open_directory(self, file_path):
        if not os.path.isfile(file_path):
            if not self.scheduled:
                error = QMessageBox()
                error.setText("Error: File does not exist.")
                error.exec_()
                with open(DIRECTORY_FILE, "r") as f:
                    paths = f.read().splitlines()
                if file_path in paths:
                    paths.remove(file_path)
                    with open(DIRECTORY_FILE, "w") as f:
                        f.writelines(p + "\n" for p in paths)
                self.deleted_file.emit(file_path)
                self.deleteLater()
        else:
            self.canvas_window.label.loadImage(file_path)

    def ocr(self):
        self.canvas_window.label.current_canvas_image = self.canvas_window.label.canvas.toImage()
        if self.canvas_window.label.hasChanged() or self.file_path == "":
            self.savePopup()
        if not self.canvas_window.label.hasChanged():
            ocr_findings = pytesseract.image_to_string(Image.open(self.file_path))
            ocr_prompt = QtWidgets.QDialog(self)
            ocr_prompt.setWindowTitle("Typed Characters found (OCR)")
            options = QtWidgets.QDialogButtonBox.Close
            ocr_prompt.buttonBox = QtWidgets.QDialogButtonBox(options)
            ocr_prompt.buttonBox.rejected.connect(ocr_prompt.reject)
            ocr_prompt.layout = QtWidgets.QVBoxLayout()
            label = QLabel(ocr_prompt)
            label.setText("Found: \n" + ocr_findings)
            ocr_prompt.layout.addWidget(label)
            ocr_prompt.layout.addWidget(ocr_prompt.buttonBox)
            ocr_prompt.setLayout(ocr_prompt.layout)
            ocr_prompt.exec_()
        else:
            return
