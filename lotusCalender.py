import sys
from getpass import getpass

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QDialogButtonBox, QVBoxLayout, QHBoxLayout, \
    QDialog, QGridLayout, QGroupBox, QFormLayout, QTextEdit, QSpinBox, QDateTimeEdit, QLineEdit, QTimeEdit, QCheckBox, \
    QRadioButton, QErrorMessage, QMessageBox, QLabel, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QRect, QTime, QDate
import json

SCHEDULE_FILE_PATH = "schedule.json"

class UICalendarWindow(QWidget):
    def __init__(self, parent=None):
        super(UICalendarWindow, self).__init__(parent)

        # self.setObjectName("Form")
        # self.resize(640, 480)

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

        print(self.schedule)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.widget.setObjectName("widget")

        self.main_layout = QtWidgets.QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")

        self.setLayout(self.main_layout)

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_layout.setObjectName("bottom_layout")

        self.bottom_left_layout = QtWidgets.QVBoxLayout()
        self.bottom_left_layout.setObjectName("bottom_left_layout")

        self.schedule_table = QtWidgets.QGridLayout()
        self.schedule_table.setObjectName("schedule_table")

        headers = ["Class", "Block(s)", "Actions"]
        for i in range(0, len(headers)):
            self.schedule_table.addWidget(QLabel(headers[i]), 0, i)

        self.calendarWidget = QtWidgets.QCalendarWidget(self.widget)
        self.calendarWidget.setObjectName("calendarWidget")

        self.update_from_file()

        self.bottom_left_layout.addLayout(self.schedule_table)

        vertical_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.bottom_left_layout.addItem(vertical_spacer)

        self.add_schedule_button = QtWidgets.QPushButton(self.widget)
        self.add_schedule_button.setObjectName("add_schedule_button")
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
            print("Data", self.schedule)
            with open(SCHEDULE_FILE_PATH, "w+") as self.schedule_file:
                json.dump(self.schedule, self.schedule_file, indent=4, sort_keys=True)
            self.schedule_file.close()
            self.update_from_file()


class DayPicker(QWidget):
    def __init__(self):
        super(DayPicker, self).__init__()
        self.layout = QHBoxLayout()
        weekends = False
        days = ["M", "T", "W", "R", "F", "Sa" if weekends else None, "Su" if weekends else None]
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
        self.rows_before_blocks = 2

        #Class Title
        self.name_edit = QLineEdit()
        self.layout.addRow("Class Name:", self.name_edit)

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
        print(old_blocks, self.blocks)
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
                # Check for duplicate blocks
                found_duplicate = False
                for other in range(self.rows_before_blocks, self.layout.rowCount() - 1):
                    if row == other:
                        continue
                    other_block_widget = self.layout.itemAt(other, QFormLayout.FieldRole).widget()
                    same_time = block_widget.get_time() == other_block_widget.get_time()
                    same_day = block_widget.day_picker.get_day() == other_block_widget.day_picker.get_day()
                    if same_time and same_day:
                        found_duplicate = True
                        error = QMessageBox()
                        error.setText("Block {} and {} cannot have the same day and time.".format(row - self.rows_before_blocks + 1, other - self.rows_before_blocks + 1))
                        error.exec_()
                        break
                if found_duplicate:
                    return
        super(Popup, self).accept()

    def reject(self):
        super(Popup, self).reject()
