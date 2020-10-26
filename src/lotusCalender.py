import json
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTime, QDate, pyqtSignal, QRect, QRectF
from PyQt5.QtGui import QColor, QPolygon, QPen
from PyQt5.QtWidgets import QPushButton, QWidget, QDialogButtonBox, QVBoxLayout, QHBoxLayout, \
    QDialog, QFormLayout, QSpinBox, QDateTimeEdit, QLineEdit, QTimeEdit, QRadioButton, QMessageBox, QLabel, \
    QCalendarWidget, QStackedWidget, QColorDialog
from src.constants import SCHEDULE_FILE_PATH

DAYS = ["M", "T", "W", "R", "F", "Sa", "Su"]

class UICalendarWindow(QWidget):
    def __init__(self, parent=None):
        super(UICalendarWindow, self).__init__(parent)

        #Schedule file creation/loading
        try:
            self.schedule_file = open(SCHEDULE_FILE_PATH)
            self.schedule = json.load(self.schedule_file)
            self.schedule_file.close()
        except FileNotFoundError as e:
            with open(SCHEDULE_FILE_PATH, "w+") as self.schedule_file:
                self.schedule_file.write("[]")
            self.schedule_file.close()
            with open(SCHEDULE_FILE_PATH, "r") as self.schedule_file:
                self.schedule = json.load(self.schedule_file)
            self.schedule_file.close()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 640, 480))

        self.main_layout = QtWidgets.QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)

        self.bottom_layout = QtWidgets.QHBoxLayout()

        self.bottom_left_layout = QtWidgets.QVBoxLayout()

        self.schedule_table = ScheduleTable()

        self.stackedWidget = QStackedWidget()
        self.calendarWidget = ScheduleCalendar(self.schedule, self.stackedWidget, parent=self)
        self.stackedWidget.addWidget(self.calendarWidget)

        self.update_from_file()

        self.bottom_left_layout.addWidget(self.schedule_table)

        vertical_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.bottom_left_layout.addItem(vertical_spacer)

        self.add_schedule_button = QtWidgets.QPushButton(self.widget)
        self.add_schedule_button.setText("Add New Scheduled Notes")
        self.add_schedule_button.clicked.connect(self.addNotes)

        self.bottom_left_layout.addWidget(self.add_schedule_button)

        self.bottom_layout.addLayout(self.bottom_left_layout)

        add_schedule_button_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.bottom_layout.addItem(add_schedule_button_spacer)

        self.bottom_layout.addWidget(self.stackedWidget)

        self.main_layout.addLayout(self.bottom_layout)

        self.update_from_file()
        self.show()

    def update_from_file(self):
        #Update table
        with open(SCHEDULE_FILE_PATH) as self.schedule_file:
            self.schedule = json.load(self.schedule_file)
        self.calendarWidget.updateSchedule(self.schedule)
        self.schedule_table.updateTable(self.schedule)

    def addNotes(self):
        popup = Popup()
        result = popup.exec_()
        if result:
            data = popup.get_data()
            self.schedule.append(data)
            with open(SCHEDULE_FILE_PATH, "w+") as self.schedule_file:
                json.dump(self.schedule, self.schedule_file, indent=4, sort_keys=True)
            self.schedule_file.close()
            self.update_from_file()

class ScheduleTable(QWidget):
    def __init__(self):
        super(ScheduleTable, self).__init__()
        self.layout = QtWidgets.QGridLayout()

        headers = ["Class", "Block(s)"]
        for i in range(0, len(headers)):
            self.layout.addWidget(QLabel(headers[i]), 0, i)
        self.setLayout(self.layout)

    def updateTable(self, schedule):
        for i in range(0, len(schedule)):
            cls = schedule[i]
            # Add name to table
            class_name = QPushButton(cls["name"])
            class_name.setStyleSheet("background-color: rgb({},{},{})".format(cls["color"]["r"],
                                                                              cls["color"]["g"],
                                                                              cls["color"]["b"]))
            class_name.clicked.connect(lambda state, x=cls: self.editClass(x))
            #print(cls["name"])
            self.layout.addWidget(class_name, i + 1, 0)
            # Add Blocks
            block_string = ""
            for j in range(0, len(cls["blocks"])):
                b = cls["blocks"][j]
                block_string += "{} {}{}".format(b["day"],
                                                  QTime(b["time"]["hour"], b["time"]["minute"]).toString("hh:mm AP"),
                                                  ", " if j != len(cls["blocks"]) - 1 else "")
                self.layout.addWidget(QLabel(block_string), i + 1, 1)

    def editClass(self, cls):
        popup = Popup(cls=cls)
        results = popup.exec_()
        if results:
            pass
        pass


def isClassDate(cls, date : QDate):
    start_date = QDate(cls["start"]["year"], cls["start"]["month"], cls["start"]["day"])
    end_date = QDate(cls["end"]["year"], cls["end"]["month"], cls["end"]["day"])
    if start_date <= date <= end_date:
        for b in cls["blocks"]:
            if b["day"] == DAYS[date.dayOfWeek() - 1]:
                return True
    return False

class DayViewer(QWidget):
    back = pyqtSignal()

    def __init__(self, date : QDate, schedule, parent=None):
        super(QWidget, self).__init__()
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back.emit)
        top_layout.addWidget(back_button, 0, Qt.AlignRight)

        top_layout.addWidget(QLabel(date.toString("Classes for MMMM d, yyyy")), 0, Qt.AlignCenter)
        layout.addLayout(top_layout)

        self.buttons = []
        for cls in schedule:
            start_date = QDate(cls["start"]["year"], cls["start"]["month"], cls["start"]["day"])
            end_date = QDate(cls["end"]["year"], cls["end"]["month"], cls["end"]["day"])
            if start_date <= date <= end_date:
                for b in cls["blocks"]:
                    if b["day"] == DAYS[date.dayOfWeek() - 1]:
                        # Class on this day
                        button = QPushButton("{} {}".format(cls["name"], QTime(b["time"]["hour"], b["time"]["minute"]).toString("HH:mm AP")))
                        button.setStyleSheet("background-color: rgb({},{},{})".format(cls["color"]["r"],
                                                                                      cls["color"]["g"],
                                                                                      cls["color"]["b"]))
                        self.buttons.append((button, cls, date))
                        layout.addWidget(button)

        self.setLayout(layout)

class ScheduleCalendar(QCalendarWidget):
    buttonsUpdated = pyqtSignal(list)

    def __init__(self, schedule : list, stack : QStackedWidget, parent=None):
        super(ScheduleCalendar, self).__init__()
        self.schedule = schedule
        self.activated.connect(self.openDayViewer)
        self.stack = stack
        self.setGridVisible(True)

    def updateSchedule(self, schedule):
        self.schedule = schedule

    def paintCell(self, painter, rect, date):
        blocks = []
        for cls in self.schedule:
            if isClassDate(cls, date):
                for b in cls["blocks"]:
                    if b["day"] == DAYS[date.dayOfWeek() - 1]:
                        blocks.append((cls["color"], b))
        blocks.sort(key = lambda x: x[1]["time"]["hour"])
        for color, b in blocks:
            painter.setBrush(QColor(color["r"], color["g"], color["b"]))
            atop = rect.top() + ((blocks.index((color, b)) / len(blocks)) * (rect.height()))
            height = rect.height() / len(blocks)
            block_rect = QRectF(rect.left(), atop, rect.width(), height)
            painter.setPen(Qt.NoPen)
            painter.drawRect(block_rect)
        painter.setPen(QPen())
        painter.drawText(QRect(rect), Qt.TextSingleLine|Qt.AlignCenter, str(date.day()))

    def openDayViewer(self, date : QDate):
        for cls in self.schedule:
            if isClassDate(cls, date):
                self.day_viewer = DayViewer(date, self.schedule, parent=self)
                self.day_viewer.back.connect(lambda: self.stack.removeWidget(self.day_viewer))
                self.buttonsUpdated.emit(self.day_viewer.buttons)
                self.stack.addWidget(self.day_viewer)
                self.stack.setCurrentWidget(self.day_viewer)
                break

class DayPicker(QWidget):
    def __init__(self):
        super(DayPicker, self).__init__()
        self.layout = QHBoxLayout()
        weekends = False
        days = DAYS[0:len(DAYS) if weekends else 5]
        self.buttons = []
        for day in days:
            if day is not None:
                radio = QRadioButton()
                radio.setText(day)
                self.buttons.append(radio)
                self.layout.addWidget(radio)
        self.setLayout(self.layout)

    def get_day(self):
        for button in self.buttons:
            if button.isChecked():
                return button.text()

class ClassTimePicker(QWidget):
    def __init__(self):
        super(ClassTimePicker, self).__init__()
        self.layout = QHBoxLayout()
        self.time_selector = QTimeEdit()
        self.time_selector.setDisplayFormat("hh:mm AP")
        self.time_selector.setTime(QTime(12, 0, 0))
        self.layout.addWidget(self.time_selector)
        self.day_picker = DayPicker()
        self.layout.addWidget(self.day_picker)
        self.setLayout(self.layout)

    def get_time(self):
        return self.time_selector.time()

    def set_time(self, time):
        self.time_selector.setTime(QTime(time["hour"], time["minute"]))

    def set_day(self, day):
        for b in self.day_picker.buttons:
            if b.text() == day:
                b.click()

    def is_valid(self):
        return self.day_picker.get_day() is not None

class Popup(QDialog):
    def __init__(self, parent=None, cls=None):
        super(Popup, self).__init__(parent)
        self.cls = cls
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setWindowTitle("Add New Scheduled Notes" if cls is None else "Edit {} Details".format(cls["name"]))

        self.layout = QFormLayout()

        #The amount of fields in the form that come before the block section (name, #blocks, start, end date, color)
        self.rows_before_blocks = 5

        #Class Title
        self.name_edit = QLineEdit()
        self.layout.addRow("Class Name:", self.name_edit)

        #Class start and end dates
        self.start_date = QDateTimeEdit(QDate.currentDate())
        self.start_date.setDisplayFormat("MMM d yyyy")
        self.layout.addRow("Start Date:", self.start_date)
        self.end_date = QDateTimeEdit(QDate.currentDate())
        self.end_date.setDisplayFormat("MMM d yyyy")
        self.layout.addRow("End Date:" , self.end_date)

        #Color
        self.color_picker = QColorDialog()
        self.color_button = QPushButton("Pick Color")
        self.color_button.clicked.connect(self.color_picker.open)
        self.color_picker.currentColorChanged.connect(self.updateColor)
        self.layout.addRow("Color Code:", self.color_button)

        #Blocks
        self.blocks = 1
        spin_box = QSpinBox()
        spin_box.setValue(1)
        spin_box.setMinimum(1)
        spin_box.setMaximum(7)
        spin_box.valueChanged.connect(self.updateBlocks)
        self.layout.addRow("Weekly Blocks:", spin_box)
        #Class DateTime
        self.layout.addRow("Block Time:", ClassTimePicker())

        #Buttons
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.buttonBox.setOrientation(Qt.Horizontal)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        #Update Values if cls is defined
        if cls:
            self.name_edit.setText(cls["name"])
            self.start_date.setDate(QDate(cls["start"]["year"], cls["start"]["month"], cls["start"]["day"]))
            self.end_date.setDate(QDate(cls["end"]["year"], cls["end"]["month"], cls["end"]["day"]))
            self.color_picker.setCurrentColor(QColor(cls["color"]["r"], cls["color"]["g"], cls["color"]["b"]))
            spin_box.setValue(len(cls["blocks"]))
            for i in range(0, len(cls["blocks"])):
                w : ClassTimePicker = self.layout.itemAt(self.rows_before_blocks + i, QFormLayout.FieldRole).widget()
                block = cls["blocks"][i]
                w.set_day(block["day"])
                w.set_time(block["time"])

    def updateColor(self):
        self.color_button.setStyleSheet("background-color: rgb({},{},{})".format(self.color_picker.currentColor().red(),
                                                                                 self.color_picker.currentColor().green(),
                                                                                 self.color_picker.currentColor().blue()))

    def updateBlocks(self, value):
        old_blocks = self.blocks
        self.blocks = value
        rows = self.layout.rowCount()
        if self.blocks > old_blocks:
            #Change label of block 1
            if old_blocks == 1:
                self.layout.itemAt(self.rows_before_blocks, QFormLayout.LabelRole).widget().setText("Block 1 Time:")
            for i in range(1, self.blocks - old_blocks + 1):
                self.layout.insertRow(rows - 2 + i, "Block {} Time:".format(old_blocks + i), ClassTimePicker())
        elif self.blocks < old_blocks:
            if self.blocks == 1:
                self.layout.itemAt(self.rows_before_blocks, QFormLayout.LabelRole).widget().setText("Block Time:")
            rows = self.layout.rowCount()
            for i in range(1, old_blocks - self.blocks + 1):
                self.layout.removeRow(rows - (1 + i))
        self.resize(self.sizeHint())

    def get_name(self):
        return self.name_edit.text()

    def get_data(self):
        block_data = []
        for row in range(self.rows_before_blocks, self.layout.rowCount() - 1):
            block_widget : ClassTimePicker = self.layout.itemAt(row, QFormLayout.FieldRole).widget()
            time = block_widget.get_time()
            block_data.append({
                "day": block_widget.day_picker.get_day(),
                "time": {
                    "hour": time.hour(),
                    "minute": time.minute()
                }
            })
        data = {
            "name": self.get_name(),
            "blocks": block_data,
            "start": {
                "day": self.start_date.date().day(),
                "month": self.start_date.date().month(),
                "year": self.start_date.date().year()
            },
            "end": {
                "day": self.end_date.date().day(),
                "month": self.end_date.date().month(),
                "year": self.end_date.date().year()
            },
            "color": {
                "r": self.color_picker.currentColor().red(),
                "g": self.color_picker.currentColor().green(),
                "b": self.color_picker.currentColor().blue(),
            }
        }
        return data

    def accept(self):
        # TODO: Allow for saving of edits
        if self.cls is not None:
            error = QMessageBox()
            error.setText("Changes will not be saved because this feature is incomplete.")
            error.exec_()
            super(Popup, self).reject()
        # Valid name
        if len(self.get_name()) == 0:
            error = QMessageBox()
            error.setText("Please enter a class name.")
            error.exec_()
            self.name_edit.setFocus()
            return
        # TODO: Add checking for duplicate class names
        elif self.start_date.date() >= self.end_date.date():
            error = QMessageBox()
            error.setText("End date cannot {} start date.".format("be equal to" if self.start_date.date() == self.end_date.date() else "come before"))
            error.exec_()
            self.end_date.setFocus()
            return
        else:
            # Valid block times
            for row in range(self.rows_before_blocks, self.layout.rowCount() - 1):
                block_widget = self.layout.itemAt(row, QFormLayout.FieldRole).widget()
                #Make sure a day is selected
                if not block_widget.is_valid():
                    block_name = "the class block" if self.blocks == 1 else str.lower(self.layout.itemAt(row, QFormLayout.LabelRole).widget().text()).replace(" time:", "")
                    error = QMessageBox()
                    error.setText("Please select a valid day for {}.".format(block_name))
                    error.exec_()
                    return
                # Check for duplicate blocks
                for other in range(self.rows_before_blocks, self.layout.rowCount() - 1):
                    if row == other:
                        continue
                    other_block_widget = self.layout.itemAt(other, QFormLayout.FieldRole).widget()
                    same_time = block_widget.get_time() == other_block_widget.get_time()
                    same_day = block_widget.day_picker.get_day() == other_block_widget.day_picker.get_day()
                    if same_time and same_day:
                        error = QMessageBox()
                        error.setText("Block {} and {} cannot have the same day and time.".format(row - self.rows_before_blocks + 1, other - self.rows_before_blocks + 1))
                        error.exec_()
                        return
        super(Popup, self).accept()

    def reject(self):
        super(Popup, self).reject()
