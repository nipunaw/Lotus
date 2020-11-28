import json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTime, QDate, pyqtSignal, QRect, QRectF, QObject, pyqtProperty, QDateTime
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QPushButton, QWidget, QDialogButtonBox, QVBoxLayout, QHBoxLayout, \
    QDialog, QFormLayout, QSpinBox, QDateTimeEdit, QLineEdit, QTimeEdit, QRadioButton, QMessageBox, QLabel, \
    QCalendarWidget, QStackedWidget, QColorDialog, QSizePolicy, QSpacerItem, QGridLayout, QCheckBox, QMenu, QAction

from src.constants import SCHEDULE_FILE_PATH
from src.lotusUtils import clear_layout

DAYS = ["M", "T", "W", "R", "F", "Sa", "Su"]


def to_qdate(date_object:dict):
    return QDate(date_object["year"], date_object["month"], date_object["day"])

def to_qtime(date_object:dict):
    return QTime(date_object["hour"], date_object["minute"])

def to_qcolor(data_object:dict):
    return QColor(data_object["r"], data_object["g"], data_object["b"])

class Schedule(QObject):
    updated = pyqtSignal()
    connect_buttons = pyqtSignal(list)
    def __init__(self):
        super(QObject, self).__init__()
        self.load_schedule()
        self.schedule:dict = self._schedule

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, schedule:dict):
        with open(SCHEDULE_FILE_PATH, "w+") as schedule_file:
            json.dump(schedule, schedule_file, indent=4, sort_keys=True)
        schedule_file.close()
        self._schedule:dict = schedule
        self.updated.emit()

    def load_schedule(self):
        try:
            schedule_file = open(SCHEDULE_FILE_PATH)
            self._schedule = json.load(schedule_file)
            schedule_file.close()
        except FileNotFoundError as e:
            with open(SCHEDULE_FILE_PATH, "w+") as schedule_file:
                schedule_file.write("{}")
            schedule_file.close()
            with open(SCHEDULE_FILE_PATH, "r") as schedule_file:
                self._schedule = json.load(schedule_file)
            schedule_file.close()

    def get_recurring_event_start_end_dates(self, event_data:dict):
        return to_qdate(event_data["start"]), to_qdate(event_data["end"])

    def is_recurring_event_date(self, event_data:dict, date:QDate):
        event_type = event_data["type"]
        start_date, end_date = self.get_recurring_event_start_end_dates(event_data)
        if start_date <= date <= end_date:
            day_of_week = DAYS[date.dayOfWeek() - 1]
            if event_type == "class":
                for b in event_data["blocks"]:
                    if b["day"] == day_of_week:
                        return True
            elif event_type == "recurring event":
                if event_data["day"] == day_of_week:
                    return True
        return False

    def get_event_stylesheet(self, event_name:str):
        return "background-color: rgb({},{},{})".format(self._schedule[event_name]["color"]["r"],
                                                        self._schedule[event_name]["color"]["g"],
                                                        self._schedule[event_name]["color"]["b"])

    def get_event_button(self, event_name:str, time:QTime, include_time=True):
        time_string = time.toString("HH:mm AP")
        button_title = "{}{}".format(event_name, " " + time_string if include_time else "")
        button = QPushButton(button_title)
        button.setStyleSheet(self.get_event_stylesheet(event_name))
        return button

    def get_event_buttons(self, date:QDate, include_times=True):
        buttons = []
        for event_name, data in self._schedule.items():
            if data["type"] == "class":
                start_date, end_date = self.get_recurring_event_start_end_dates(data)
                if start_date <= date <= end_date:
                    for b in data["blocks"]:
                        if b["day"] == DAYS[date.dayOfWeek()-1]:
                            # Class on this day
                            time = to_qtime(b["time"])
                            button = self.get_event_button(event_name, time, include_times)
                            buttons.append((button, event_name, date, time))
            else:
                pass
                # if to_qdate(data["date"]) == date:
                #     time = to_qtime(data["time"])
                #     button = self.get_event_button(event_name, time, include_times)
                #     buttons.append((button, event_name, date, time))
        self.connect_buttons.emit(buttons)
        return buttons

    def add_event(self, data:dict):
        event_name = data["name"]
        if event_name in self._schedule.keys():
            return False
        else:
            data.pop("name")
            self._schedule[event_name] = data
            self.schedule = self._schedule
            return True

    def edit_event(self, data:dict):
        event_name = data["name"]
        data.pop("name")
        self._schedule[event_name] = data
        self.schedule = self._schedule
        return True


class UICalendarWindow(QWidget):
    def __init__(self, schedule:Schedule, parent=None):
        super(UICalendarWindow, self).__init__(parent)

        self.schedule = schedule

        self.layout = QtWidgets.QGridLayout()

        self.bottom_left_layout = QtWidgets.QVBoxLayout()

        self.schedule_table = ScheduleTable(self.schedule)
        self.schedule.updated.connect(self.schedule_table.update_table)

        self.layout.addWidget(self.schedule_table)

        self.add_schedule_button = QPushButton("Add New Scheduled Notes")
        self.add_schedule_button.clicked.connect(self.add_notes)
        self.layout.addWidget(self.add_schedule_button)

        self.setLayout(self.layout)
        self.show()

    def add_notes(self):
        popup = Popup(self.schedule)
        result = popup.exec_()
        if result:
            data = popup.get_data()
            self.schedule.add_event(data)

class ScheduleTable(QWidget):
    def __init__(self, schedule:Schedule):
        super(ScheduleTable, self).__init__()
        self.schedule = schedule
        self.schedule.updated.connect(self.update_table)
        self.grid_layout = None
        self.update_table()

    def edit_class(self, data):
        popup = Popup(self.schedule, data=data)
        popup.exec_()

    def update_table(self):
        if self.grid_layout is not None:
            pass
        self.grid_layout = QtWidgets.QGridLayout()
        self.setLayout(self.grid_layout)
        headers = ["Class", "Block(s)"]
        for i in range(0, len(headers)):
            header_label = QLabel(headers[i])
            header_label.setAlignment(Qt.AlignLeft)
            self.grid_layout.addWidget(header_label, 0, i)
        # Add Classes to Table
        for i, (class_name, data) in enumerate(self.schedule.schedule.items()):
            if data["type"] != "class":
                continue
            # Add name to table
            button = QPushButton(class_name)
            button.setStyleSheet(self.schedule.get_event_stylesheet(class_name))
            button.clicked.connect(lambda state, x=data: self.edit_class(x))
            self.grid_layout.addWidget(button, i + 1, 0)
            # Add Blocks
            block_string = ""
            days = {}
            for b in data["blocks"]:
                if b["day"] in days.keys():
                    days[b["day"]].append(b)
                else:
                    days[b["day"]] = [b]
            class_string = ""
            for j, day in enumerate(sorted(days.keys(), key=DAYS.index)):
                day_string = day + ": "
                for k, b in enumerate(days[day]):
                    day_string += QTime(b["time"]["hour"], b["time"]["minute"]).toString("hh:mmAP") + (", " if k != len(days[day]) - 1 else "")
                class_string += day_string + ("  " if j != len(days.keys()) - 1 else "")
            self.grid_layout.addWidget(QLabel(class_string), i+1, 1)

class DayViewer(QWidget):
    back = pyqtSignal()
    def __init__(self, date : QDate, schedule:Schedule, parent=None):
        super(QWidget, self).__init__()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back.emit)
        layout.addWidget(back_button, 0, 0)
        layout.addWidget(QLabel(date.toString("Classes for MMMM d, yyyy")), 0, 1)
        for i, (button, _, _, _) in enumerate(schedule.get_event_buttons(date)):
            layout.addWidget(button, i+1, 0, 1, 3)
        self.setLayout(layout)

class ScheduleCalendar(QCalendarWidget):
    def __init__(self, schedule:Schedule, stack:QStackedWidget, parent=None):
        super(ScheduleCalendar, self).__init__()
        self.schedule = schedule
        self.activated.connect(self.open_day_viewer)
        self.stack = stack
        self.setGridVisible(True)
        self.day_viewer = None

    def paintCell(self, painter, rect, date):
        blocks = []
        for event_name, data in self.schedule.schedule.items():
            event_type = data["type"]
            if event_type in ["class", "recurring event"]:
                if self.schedule.is_recurring_event_date(data, date):
                    event_blocks = []
                    if event_type == "class":
                        event_blocks = data["blocks"]
                    else:
                        event_blocks.append({
                            "day": data["day"],
                            "time": data["time"]
                        })
                    for b in event_blocks:
                        if b["day"] == DAYS[date.dayOfWeek() - 1]:
                            blocks.append({
                                "type": "class",
                                "color": data["color"],
                                "time": b["time"]
                            })
            else:
                event_date = to_qdate(data["date"])
                if date == event_date:
                    blocks.append({
                        "type": "event",
                        "color": data["color"],
                        "time": data["time"]
                    })
        blocks.sort(key = lambda x: x["time"]["hour"])
        for block in blocks:
            color = block["color"]
            painter.setBrush(to_qcolor(color))
            atop = rect.top() + ((blocks.index(block) / len(blocks)) * (rect.height()))
            height = rect.height() / len(blocks)
            block_rect = QRectF(rect.left(), atop, rect.width(), height)
            painter.setPen(Qt.NoPen)
            painter.drawRect(block_rect)
        painter.setPen(QPen())
        # noinspection PyCallingNonCallable
        painter.drawText(QRect(rect), Qt.TextSingleLine|Qt.AlignCenter, str(date.day()))

    def open_day_viewer(self, date:QDate):
        for event_name, data in self.schedule.schedule.items():
            if self.schedule.is_recurring_event_date(event_name, date):
                self.day_viewer = DayViewer(date, self.schedule, parent=self)
                self.day_viewer.back.connect(lambda: self.stack.removeWidget(self.day_viewer))
                self.stack.addWidget(self.day_viewer)
                self.stack.setCurrentWidget(self.day_viewer)
                break

class DayPicker(QWidget):
    def __init__(self):
        super(DayPicker, self).__init__()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        weekends = True
        days = DAYS[0:len(DAYS) if weekends else 5]
        self.buttons = []
        for day in days:
            if day is not None:
                radio = QRadioButton()
                radio.sizePolicy().setRetainSizeWhenHidden(False)
                radio.setText(day)
                self.buttons.append(radio)
                self.layout.addWidget(radio)

    def get_day(self):
        for button in self.buttons:
            if button.isChecked():
                return button.text()

class ClassTimePicker(QWidget):
    def __init__(self, parent=None):
        super(ClassTimePicker, self).__init__(parent=parent)
        self.time_selector = QTimeEdit()
        self.time_selector.sizePolicy().setRetainSizeWhenHidden(False)
        self.time_selector.setDisplayFormat("hh:mm AP")
        self.time_selector.setTime(QTime(12, 0, 0))

        self.day_picker = DayPicker()
        self.day_picker.sizePolicy().setRetainSizeWhenHidden(False)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.time_selector)
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

class DateTimePickerSeriesModel(QObject):
    def __init__(self, parent=None):
        super(DateTimePickerSeriesModel, self).__init__(parent)
        self._content = QDateTime.currentDateTime()

    contentChanged = pyqtSignal(QDateTime)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, date_time:QDateTime):
        self._content = date_time
        self.contentChanged.emit(self._content)

class DateTimePickerSeries(QWidget):
    def __init__(self, model, display:str):
        super(DateTimePickerSeries, self).__init__()
        self.model = model

        date_time = QDateTimeEdit(self.model.content)
        date_time.setDisplayFormat(display)
        date_time.dateTimeChanged.connect(self.set_model_date_time)

        self.model.contentChanged.connect(date_time.setDateTime)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(date_time)
        self.setLayout(layout)

    def set_model_date_time(self, date_time:QDateTime):
        self.model.content = date_time

class Popup(QDialog):
    def __init__(self, schedule:Schedule, parent=None, data=None):
        super(Popup, self).__init__(parent)
        self.schedule = schedule
        self.data, self.class_name = data if data is not None else (None, None)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setWindowTitle("Add New Scheduled Notes" if data is None else "Edit {} Details".format(self.class_name))

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 0, 0, self.form_layout.verticalSpacing())
        self.form_layout_widget = QWidget()
        self.form_layout_widget.setLayout(self.form_layout)

        #The amount of fields in the form that come before the block section (name, #blocks, start, end date, color)
        self.rows_before_blocks = 3

        self.event_type = QPushButton()
        event_type_menu = QMenu()
        event_type_menu.addAction("Class")
        event_type_menu.addSection("Event")
        event_type_menu.addAction("One Time Event")
        event_type_menu.addAction("Recurring Event")
        event_type_menu.addAction("One Time Class Event")
        for action in event_type_menu.actions():
            if not action.isSeparator():
                action.triggered.connect(lambda state, x=action.text(): self.set_type(x))
        self.event_type.setMenu(event_type_menu)
        self.form_layout.addRow("Type:", self.event_type)

        #Class Title
        self.name_edit = QLineEdit()
        self.form_layout.addRow("Name:", self.name_edit)
        #Color
        self.color_picker = QColorDialog()
        self.color_button = QPushButton("Pick Color")
        self.color_button.clicked.connect(self.color_picker.open)
        self.color_picker.currentColorChanged.connect(self.update_color)
        self.form_layout.addRow("Color Code:", self.color_button)

        # Initialize widgets to be added later
        self.start_date_model = DateTimePickerSeriesModel(self)
        self.class_start_date = DateTimePickerSeries(self.start_date_model, "MMM d yyyy")
        self.event_start_date = DateTimePickerSeries(self.start_date_model, "MMM d yyyy")

        self.end_date_model = DateTimePickerSeriesModel(self)
        self.class_end_date = DateTimePickerSeries(self.end_date_model, "MMM d yyyy")
        self.event_end_date = DateTimePickerSeries(self.end_date_model, "MMM d yyyy")

        self.event_date_model = DateTimePickerSeriesModel(self)
        self.class_event_date = DateTimePickerSeries(self.event_date_model, "MMM d yyyy hh:mm:AP")
        self.event_date = DateTimePickerSeries(self.event_date_model, "MMM d yyyy hh:mm:AP")

        # Blocks
        self.blocks = 1
        self.spin_box = QSpinBox()
        self.spin_box.setValue(1)
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(7)
        self.spin_box.valueChanged.connect(self.update_blocks)

        self.class_picker = QPushButton()
        class_picker_menu = QMenu()
        for class_name in self.schedule.schedule.keys():
            class_action = QAction(class_name, parent=class_picker_menu)
            class_action.triggered.connect(lambda state, x=class_action.text(): self.class_picker.setText(x))
            class_picker_menu.addAction(class_action)
        class_picker_menu.aboutToShow.connect(
            lambda: class_picker_menu.setMinimumWidth(self.class_picker.width()))
        self.class_picker.setMenu(class_picker_menu)

        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0, 0, 0, 0)

        class_layout = QFormLayout()
        class_layout.setContentsMargins(0, 0, 0, class_layout.verticalSpacing())
        class_layout.addRow("Start Date:", self.class_start_date)
        class_layout.addRow("End Date:", self.class_end_date)
        class_layout.addRow("Weekly Blocks:", self.spin_box)
        class_layout.addRow("Block Time:", ClassTimePicker())
        self.class_options = QWidget()
        self.class_options.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.class_options.setLayout(class_layout)

        recurring_event_layout = QFormLayout()
        recurring_event_layout.setContentsMargins(0, 0, 0, recurring_event_layout.verticalSpacing())
        recurring_event_layout.addRow("Start Date:", self.event_start_date)
        recurring_event_layout.addRow("End Date:", self.event_end_date)
        self.recurring_event_time_picker = ClassTimePicker()
        recurring_event_layout.addRow("Event Time:", self.recurring_event_time_picker)
        self.recurring_event_options = QWidget()
        self.recurring_event_options.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.recurring_event_options.setLayout(recurring_event_layout)

        one_time_event_layout = QFormLayout()
        one_time_event_layout.setContentsMargins(0, 0, 0, one_time_event_layout.verticalSpacing())
        one_time_event_layout.addRow("Event Date:", self.event_date)
        self.one_time_event_options = QWidget()
        self.one_time_event_options.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.one_time_event_options.setLayout(one_time_event_layout)

        class_event_layout = QFormLayout()
        class_event_layout.setContentsMargins(0, 0, 0, class_event_layout.verticalSpacing())
        class_event_layout.addRow("Class:", self.class_picker)
        class_event_layout.addRow("Event Date:", self.class_event_date)
        self.class_event_options = QWidget()
        self.class_event_options.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.class_event_options.setLayout(class_event_layout)

        self.stack.addWidget(self.class_event_options)
        self.stack.addWidget(self.one_time_event_options)
        self.stack.addWidget(self.recurring_event_options)
        self.stack.addWidget(self.class_options)

        self.set_type("Class")

        self.layout.addWidget(self.form_layout_widget)
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)
        self.show_buttons()

        #Update Values if self.data is defined
        if self.data is not None:
            self.name_edit.setText(self.data["name"])
            self.start_date.setDate(to_qdate(self.data["start"]))
            self.end_date.setDate(to_qdate(self.data["end"]))
            self.color_picker.setCurrentColor(to_qcolor(self.data["color"]))
            self.spin_box.setValue(len(self.data["blocks"]))
            for i in range(0, len(self.data["blocks"])):
                w : ClassTimePicker = self.layout.itemAt(self.rows_before_blocks + i, QFormLayout.FieldRole).widget()
                block = self.data["blocks"][i]
                w.set_day(block["day"])
                w.set_time(block["time"])

    def show_buttons(self):
        buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.setOrientation(Qt.Horizontal)
        self.layout.addWidget(buttonBox)

    def set_type(self, event_type:str):
        if self.event_type.text() == event_type:
            return
        self.event_type.setText(event_type)
        self.stack.currentWidget().setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        if event_type == "Class":
            self.class_options.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.class_options.adjustSize()
            self.stack.setCurrentWidget(self.class_options)
        elif event_type == "Recurring Event":
            self.recurring_event_options.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.recurring_event_options.adjustSize()
            self.stack.setCurrentWidget(self.recurring_event_options)
        elif event_type == "One Time Event":
            self.one_time_event_options.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.one_time_event_options.adjustSize()
            self.stack.setCurrentWidget(self.one_time_event_options)
        elif event_type == "One Time Class Event":
            self.class_event_options.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.class_event_options.adjustSize()
            self.stack.setCurrentWidget(self.class_event_options)
        self.stack.adjustSize()
        max_width = 0
        for i in range(self.form_layout.rowCount()):
            widget = self.form_layout.itemAt(i, QFormLayout.LabelRole).widget()
            widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            widget.adjustSize()
            max_width = max(widget.size().width(), max_width)
        # noinspection PyTypeChecker
        current_widget_layout:QFormLayout = self.stack.currentWidget().layout()
        for i in range(current_widget_layout.rowCount()):
            widget = current_widget_layout.itemAt(i, QFormLayout.LabelRole).widget()
            widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            widget.adjustSize()
            max_width = max(widget.size().width(), max_width)
        for i in range(self.form_layout.rowCount()):
            self.form_layout.itemAt(i, QFormLayout.LabelRole).widget().setMinimumWidth(max_width)
        for i in range(current_widget_layout.rowCount()):
            current_widget_layout.itemAt(i, QFormLayout.LabelRole).widget().setMinimumWidth(max_width)
        self.adjustSize()

    def update_color(self):
        self.color_button.setStyleSheet("background-color: rgb({},{},{})".format(self.color_picker.currentColor().red(),
                                                                                 self.color_picker.currentColor().green(),
                                                                                 self.color_picker.currentColor().blue()))

    def update_blocks(self, value):
        if self.blocks == value:
            return
        old_blocks = self.blocks
        self.blocks = value
        class_options_layout:QFormLayout = self.class_options.layout()
        if self.blocks > old_blocks:
            #Change label of block 1
            if old_blocks == 1:
                class_options_layout.itemAt(self.rows_before_blocks, QFormLayout.LabelRole).widget().setText("Block 1 Time:")
            for i in range(1, self.blocks - old_blocks + 1):
                offset = self.rows_before_blocks + old_blocks + i - 1
                widget = class_options_layout.itemAt(offset, QFormLayout.FieldRole)
                label = class_options_layout.itemAt(offset, QFormLayout.LabelRole)
                if widget is not None and label is not None:
                    widget = widget.widget()
                    label = label.widget()
                    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    widget.adjustSize()
                    label.adjustSize()
                    widget.show()
                    label.show()
                else:
                    picker = ClassTimePicker()
                    picker.sizePolicy().setRetainSizeWhenHidden(False)
                    class_options_layout.addRow("Block {} Time:".format(old_blocks + i), picker)
        elif self.blocks < old_blocks:
            if self.blocks == 1:
                class_options_layout.itemAt(self.rows_before_blocks, QFormLayout.LabelRole).widget().setText("Block Time:")
            for i in range(old_blocks - self.blocks):
                offset = self.rows_before_blocks + old_blocks + i - 1
                widget = class_options_layout.itemAt(offset, QFormLayout.FieldRole).widget()
                label = class_options_layout.itemAt(offset, QFormLayout.LabelRole).widget()
                print(widget.size())
                widget.hide()
                label.hide()
                widget.adjustSize()
                label.adjustSize()
                self.class_options.adjustSize()
                self.stack.adjustSize()
                self.adjustSize()

                print(widget.size())

        # self.class_options.adjustSize()
        # self.stack.adjustSize()
        # self.adjustSize()

    def get_name(self):
        return self.name_edit.text()

    def get_data(self):
        event_type = self.event_type.text()
        data = {
            "type": event_type.lower(),
            "name": self.get_name(),
            "color": {
                "r": self.color_picker.currentColor().red(),
                "g": self.color_picker.currentColor().green(),
                "b": self.color_picker.currentColor().blue(),
            }
        }
        if event_type == "Class":
            block_data = []
            # noinspection PyTypeChecker
            class_layout:QFormLayout = self.stack.currentWidget().layout()
            for row in range(self.rows_before_blocks, class_layout.rowCount()):
                # noinspection PyTypeChecker
                block_widget:ClassTimePicker = class_layout.itemAt(row, QFormLayout.FieldRole).widget()
                if block_widget.isHidden():
                    continue
                time = block_widget.get_time()
                block_data.append({
                    "day": block_widget.day_picker.get_day(),
                    "time": {
                        "hour": time.hour(),
                        "minute": time.minute()
                    }
                })
            data["blocks"] = block_data
        if event_type in ["Class", "Recurring Event"]:
            start_date = self.start_date_model.content.date()
            data["start"] = {
                "day": start_date.day(),
                "month": start_date.month(),
                "year": start_date.year()
            }
            end_date = self.end_date_model.content.date()
            data["end"] = {
                "day": end_date.day(),
                "month": end_date.month(),
                "year": end_date.year()
            }
        if event_type == "Recurring Event":
            data["day"] = self.recurring_event_time_picker.day_picker.get_day()
            time = self.recurring_event_time_picker.get_time()
            data["time"] = {
                "hour": time.hour(),
                "minute": time.minute()
            }
        if event_type == "One Time Class Event":
            data["class_name"] = self.class_picker.text()
        if event_type in ["One Time Event", "One Time Class Event"]:
            date_time = self.event_date_model.content
            date = date_time.date()
            time = date_time.time()
            data["date"] = {
                "day": date.day(),
                "month": date.month(),
                "year": date.year(),
            }
            data["time"] = {
                "hour": time.hour(),
                "minute": time.minute()
            }
        return data

    def accept(self):
        event_type = self.event_type.text()
        if event_type == "":
            error = QMessageBox()
            error.setText("Please select a type for the event.")
            error.exec_()
            self.event_type.setFocus()
            return
        # Check Name
        if len(self.get_name()) == 0:
            error = QMessageBox()
            error.setText("Please enter a name for the event.")
            error.exec_()
            self.name_edit.setFocus()
            return
        if event_type in ["Class", "Recurring Event"]:
            # Check Start/End Date
            start_date = self.start_date_model.content.date()
            end_date = self.end_date_model.content.date()
            if start_date >= end_date:
                error = QMessageBox()
                error.setText("End date cannot {} start date.".format("be equal to" if start_date == end_date else "come before"))
                error.exec_()
                if event_type == "Class":
                    self.class_end_date.setFocus()
                else:
                    self.event_end_date.setFocus()
                return
            if event_type == "Class":
                # Check Blocks
                # noinspection PyTypeChecker
                class_layout:QFormLayout = self.stack.currentWidget().layout()
                print(class_layout)
                for row in range(self.rows_before_blocks, class_layout.rowCount()):
                    block_widget = class_layout.itemAt(row, QFormLayout.FieldRole).widget()
                    if block_widget.isHidden():
                        continue
                    # Make sure a day is selected for each block
                    if not block_widget.is_valid():
                        block_name = "the class block" if self.blocks == 1 else str.lower(
                            class_layout.itemAt(row, QFormLayout.LabelRole).widget().text()).replace(" time:", "")
                        error = QMessageBox()
                        error.setText("Please select a valid day for {}.".format(block_name))
                        error.exec_()
                        return
                    # Check for duplicate blocks
                    for other in range(self.rows_before_blocks, class_layout.rowCount() - 1):
                        if row == other:
                            continue
                        other_block_widget = class_layout.itemAt(other, QFormLayout.FieldRole).widget()
                        same_time = block_widget.get_time() == other_block_widget.get_time()
                        same_day = block_widget.day_picker.get_day() == other_block_widget.day_picker.get_day()
                        if same_time and same_day:
                            error = QMessageBox()
                            error.setText("Block {} and {} cannot have the same day and time.".format(
                                row - self.rows_before_blocks+1, other - self.rows_before_blocks+1))
                            error.exec_()
                            return
            if event_type == "Recurring Event":
                # Make sure a day is selected
                if not self.recurring_event_time_picker.is_valid():
                    error = QMessageBox()
                    error.setText("Please select a valid day for this event.")
                    error.exec_()
                    self.recurring_event_time_picker.setFocus()
                    return
        if event_type == "One Time Class Event":
            # Check Class
            if len(self.class_picker.text()) == 0:
                error = QMessageBox()
                error.setText("Please select a class for this event.")
                error.exec_()
                self.class_picker.setFocus()
                return
        if self.data is not None:
            error = QMessageBox()
            error.setText("Changes will not be saved because this feature is incomplete.")
            error.exec_()
            super(Popup, self).reject()
        # Valid name
        elif self.get_name() in self.schedule.schedule.keys():
            error = QMessageBox()
            error.setText("An event with this name already exists, would you like to overwrite it?")
            error.setStandardButtons(error.Apply | error.Cancel)
            result = error.exec_()
            if result == error.Apply:
                self.schedule.edit_event(self.get_data())
                self.reject()
            elif result == error.Cancel:
                self.name_edit.setFocus()
        super(Popup, self).accept()

    def reject(self):
        super(Popup, self).reject()
