import sys
from getpass import getpass

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QDialogButtonBox, QVBoxLayout, QHBoxLayout, \
    QDialog, QGridLayout, QGroupBox, QFormLayout, QTextEdit, QSpinBox, QDateTimeEdit, QLineEdit, QTimeEdit, QCheckBox, \
    QRadioButton, QErrorMessage, QMessageBox, QLabel, QTableWidgetItem, QCalendarWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QRect, QTime, QDate
import json

SCHEDULE_FILE_PATH = "../data/schedule.json"

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

        self.schedule_table = QtWidgets.QGridLayout()

        headers = ["Class", "Block(s)", "Actions"]
        for i in range(0, len(headers)):
            self.schedule_table.addWidget(QLabel(headers[i]), 0, i)

        self.calendarWidget = ScheduleCalendar(self.schedule)

        self.update_from_file()

        self.bottom_left_layout.addLayout(self.schedule_table)

        vertical_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.bottom_left_layout.addItem(vertical_spacer)

        self.add_schedule_button = QtWidgets.QPushButton(self.widget)
        self.add_schedule_button.setText("Add New Scheduled Notes")
        self.add_schedule_button.clicked.connect(self.addNotes)

        self.bottom_left_layout.addWidget(self.add_schedule_button)

        self.bottom_layout.addLayout(self.bottom_left_layout)

        add_schedule_button_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.bottom_layout.addItem(add_schedule_button_spacer)

        self.bottom_layout.addWidget(self.calendarWidget)

        self.main_layout.addLayout(self.bottom_layout)

        self.update_from_file()
        self.show()

    def update_from_file(self):
        #Update table
        with open(SCHEDULE_FILE_PATH) as self.schedule_file:
            self.schedule = json.load(self.schedule_file)
        self.calendarWidget.updateSchedule(self.schedule)
        for i in range(0, len(self.schedule)):
            cls = self.schedule[i]
            # Add name to table
            self.schedule_table.addWidget(QLabel(cls["name"]), i + 1, 0)
            # Add Blocks
            block_string = ""
            for j in range(0, len(cls["blocks"])):
                b = cls["blocks"][j]
                block_string += "{} {}{}".format(b["day"],
                                                  QTime(b["time"]["hour"], b["time"]["minute"]).toString("hh:mm AP"),
                                                  ", " if j != len(cls["blocks"]) - 1 else "")
                self.schedule_table.addWidget(QLabel(block_string), i + 1, 1)

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

class ScheduleCalendar(QCalendarWidget):
    def __init__(self, schedule : list):
        super(ScheduleCalendar, self).__init__()
        self.schedule = schedule

    def updateSchedule(self, schedule):
        self.schedule = schedule

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        for cls in self.schedule:
            start_date = QDate(cls["start"]["year"], cls["start"]["month"], cls["start"]["day"])
            end_date = QDate(cls["end"]["year"], cls["end"]["month"], cls["end"]["day"])
            if start_date <= date <= end_date:
                for b in cls["blocks"]:
                    if b["day"] == DAYS[date.dayOfWeek() - 1]:
                        painter.setBrush(QtCore.Qt.red)
                        painter.drawEllipse(rect.topLeft() + QtCore.QPoint(12, 7), 3, 3)


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

    def is_valid(self):
        return self.day_picker.get_day() is not None

class Popup(QDialog):
    def __init__(self, parent=None):
        super(Popup, self).__init__(parent)

        self.setWindowTitle("Add New Scheduled Notes")

        self.layout = QFormLayout()

        #The amount of fields in the form that come before the block section (name and #blocks)
        self.rows_before_blocks = 4

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

    def updateBlocks(self, value):
        old_blocks = self.blocks
        self.blocks = value
        if self.blocks > old_blocks:
            #Change label of block 1
            if old_blocks == 1:
                self.layout.itemAt(2, QFormLayout.LabelRole).widget().setText("Block 1 Time:")
            self.layout.insertRow(self.blocks + (self.rows_before_blocks - 1), "Block {} Time:".format(self.blocks), ClassTimePicker())
        elif self.blocks < old_blocks:
            if self.blocks == 1:
                self.layout.itemAt(2, QFormLayout.LabelRole).widget().setText("Block Time:")
            self.layout.removeRow(self.blocks + self.rows_before_blocks)
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
        }
        return data

    def accept(self):
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
