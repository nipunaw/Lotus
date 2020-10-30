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
from src.lotusPrevious import UIPreviousWindow
from src.lotusCore import *


import pytesseract
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QMessageBox, QDialog

from src import lotusCore
from src.constants import CONFIG_FILE, DIRECTORY_FILE, SCHEDULE_FILE_PATH

class UINoteWindow(QWidget):
    deleted_file = pyqtSignal(str)

    def __init__(self, directory : str, parent=None, scheduled=False):
        super(UINoteWindow, self).__init__(parent)

        # To support open previous
        self.newNoteCount = 0
        self.newNotes = []

        self.directory = directory
        self.scheduled = scheduled

        ########### Writing parameters ###########
        # General utensil parameters
        self.pen_utensil = True
        self.eraser_utensil = False
        self.utensil_press = False
        # Scrolling Parameters #
        self.mouse_button_scrolling = False
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
        self.settings_menu = self.menu_bar.addMenu("Settings")
        self.save_option = QtWidgets.QAction("Save", self)
        self.save_option.setShortcut("Ctrl+S")
        self.save_as_option = QtWidgets.QAction("Save As" if not scheduled else "Export", self)
        self.save_as_option.setShortcut("F12")
        self.open_recent_option = QtWidgets.QAction("Open Recent", self)
        self.heading_option = QtWidgets.QAction("Add/Edit Heading", self)
        self.heading_option.setShortcut("Ctrl+H")
        self.settings_option = QtWidgets.QAction("Font")
        self.settings_menu.addAction(self.settings_option)
        self.file_menu.addAction(self.save_option)
        self.file_menu.addAction(self.save_as_option)
        self.file_menu.addAction(self.open_recent_option)
        self.template_menu.addAction(self.heading_option)
        self.save_option.triggered.connect(self.save)
        self.save_as_option.triggered.connect(self.save_as)
        self.open_recent_option.triggered.connect(self.open_recent)
        self.heading_option.triggered.connect(self.heading)
        self.settings_option.triggered.connect(self.settings)
        self.open_option = QtWidgets.QAction("Open", self)
        self.file_menu.addAction(self.open_option)
        self.open_option.triggered.connect(self.open)
        self.ocr_menu = self.menu_bar.addMenu("OCR")
        self.find_ocr = QtWidgets.QAction("Find Typed/Neat Text", self)
        self.ocr_menu.addAction(self.find_ocr)
        self.find_ocr.triggered.connect(self.ocr)


        ########### Canvas color ###########
        # Handled by resizeEvent
        self.first_time = True

        ########### Saving/Opening ###########
        if self.scheduled:
            self.file_path = self.directory
        elif self.directory is not None:
            self.file_path = self.directory[:-1]
        else:
            self.file_path = ""

        self.file_path_2 = ""
        ########### Closing ###########
        self.new_strokes_since_save = False

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
        #compare_canvas = QtGui.QPixmap(self.size().width(), self.size().height())
        #compare_canvas.fill(Qt.white)
        #compare_canvas_image = compare_canvas.toImage()
        current_canvas_image = self.canvas.toImage()
        if not current_canvas_image == self.compare_canvas_image:
            self.savePopup()

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
            if (self.directory is not None and not self.scheduled) \
                    or (self.directory is not None and self.scheduled and os.path.isfile(self.directory)):
                self.open_directory(self.directory, truncate=(not self.scheduled))
        else: # Not reached
            newCanvas = self.canvas.scaled(self.size().width(), self.size().height())
            self.canvas = newCanvas
        self.compare_canvas_image = self.canvas.toImage()

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
        elif event.button() == Qt.MiddleButton:
            self.mouse_button_scrolling = True

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
        elif event.buttons() and Qt.MiddleButton and self.mouse_button_scrolling:
            pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.utensil_press = False
        elif event.button() == Qt.MiddleButton:
            self.mouse_button_scrolling = False

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
            self.compare_canvas_image = self.canvas.toImage()

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


        self.new_strokes_since_save = False
        # Saving canvas
        self.canvas.save(self.file_path)
        self.setWindowTitle(self.file_path)
        self.compare_canvas_image = self.canvas.toImage()

    # To support open previous
    def open_recent(self):
        # will replace with code that actually works
        self.PreviousWindow = UIPreviousWindow(set_paths=True)
        self.PreviousWindow.setWindowTitle("Non-Scheduled Notes")
        ##self.PreviousWindow.setCentralWidget(self.PreviousWindow)

        ########### Background color ###########
        p = self.PreviousWindow.palette()
        p.setColor(self.PreviousWindow.backgroundRole(), Qt.white)
        self.PreviousWindow.setPalette(p)

        ########### Button handling ###########
        for i in range(len(self.PreviousWindow.directories)):
            self.PreviousWindow.buttons[self.PreviousWindow.directories[i]].clicked.connect(
                lambda state, x=self.PreviousWindow.directories[i]: self.NoteWindowSeparate(x))

        self.PreviousWindow.show()

    # To support open previous
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

    # To support open previous
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
        self.new_strokes_since_save = True
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
        painter = QtGui.QPainter(self.canvas)
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
        current_canvas_image = self.canvas.toImage()
        if not current_canvas_image == self.compare_canvas_image:
            self.savePopup()
            self.file_path_2, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/home", "JPG (*.jpg);;PNG (*.png)")
            if self.file_path_2 == "":
                return
            self.file_path = self.file_path_2
            self.open_directory(self.file_path, truncate=False)
            self.setWindowTitle(self.file_path)

        else:
            self.file_path_2, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/home",
                                                                        "JPG (*.jpg);;PNG (*.png)")
            if self.file_path_2 == "":
                return
            self.file_path = self.file_path_2
            self.open_directory(self.file_path, truncate=False)
            self.setWindowTitle(self.file_path)

    def open_directory(self, file_path, truncate=True):
        if truncate:
            file_path = file_path[:-1]
        if not os.path.isfile(file_path):
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
            self.canvas = QtGui.QPixmap(file_path)
            newCanvas = self.canvas.scaled(self.size().width(), self.size().height())
            self.canvas = newCanvas
            self.compare_canvas_image = self.canvas.toImage()
            self.update()

    def ocr(self):
        current_canvas_image = self.canvas.toImage()
        if not current_canvas_image == self.compare_canvas_image or self.file_path == "":
            self.savePopup()
        if current_canvas_image == self.compare_canvas_image:
            ocr_findings = pytesseract.image_to_string(Image.open(self.file_path))
            #ocr_count = 0
            #for c in ocr_findings:
            #    if c == '.':
            #        ocr_count = ocr_count + 1
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
