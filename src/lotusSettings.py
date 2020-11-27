# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal
import configparser
from src.constants import CONFIG_FILE, assets

class UISettingsWindow(QWidget):
    pen_width_updated = pyqtSignal(int)
    eraser_width_updated = pyqtSignal(int)
    name_updated = pyqtSignal(str)

    def __init__(self, parent=None):
        super(UISettingsWindow, self).__init__(parent)
        self.setMinimumWidth(320)
        self.field_ui()

    def field_ui(self):
        self.layout = QtWidgets.QGridLayout()
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.name_field = QtWidgets.QLabel()
        self.name_field.setText("Name: ")
        #self.name_field.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.name_field.setStyleSheet("font-family: Lato")
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setText(config['DEFAULT']['name'])
        self.name_edit.setStyleSheet("font-family: Lato")

        self.pen_size = QtWidgets.QLabel()
        self.pen_size.setText("Default Pen Size: ")
        self.pen_size.setStyleSheet("font-family: Lato")
        self.pen_size_dropdown = QtWidgets.QComboBox()
        self.pen_size_dropdown.addItem("3")
        self.pen_size_dropdown.addItem("4")
        self.pen_size_dropdown.addItem("5")
        self.pen_size_dropdown.addItem("6")
        self.pen_size_dropdown.addItem("7")
        self.pen_size_dropdown.setCurrentIndex(int(config['DEFAULT']['pen_size'])-3)


        self.eraser_size = QtWidgets.QLabel()
        self.eraser_size.setText("Default Eraser Size: ")
        self.eraser_size.setStyleSheet("font-family: Lato")
        self.eraser_size_dropdown = QtWidgets.QComboBox()
        self.eraser_size_dropdown.addItem("3")
        self.eraser_size_dropdown.addItem("4")
        self.eraser_size_dropdown.addItem("5")
        self.eraser_size_dropdown.addItem("6")
        self.eraser_size_dropdown.addItem("7")
        self.eraser_size_dropdown.setCurrentIndex(int(config['DEFAULT']['eraser_size']) - 3)

        self.heading_default = QtWidgets.QLabel()
        self.heading_default.setText("New notes have name in heading ")
        self.heading_default.setStyleSheet("font-family: Lato")

        self.heading_default_checkbox = QtWidgets.QCheckBox()
        if config['DEFAULT']['name_heading'] == 'True':
            self.heading_default_checkbox.setChecked(True)
        else:
            self.heading_default_checkbox.setChecked(False)

        self.save_btn = QPushButton('Update preferences')
        self.save_btn.clicked.connect(self.update_pref)

        self.layout.addWidget(self.name_field, 0, 0)
        self.layout.addWidget(self.name_edit, 0, 1)
        self.layout.addWidget(self.pen_size, 1, 0)
        self.layout.addWidget(self.pen_size_dropdown, 1, 1)
        self.layout.addWidget(self.eraser_size, 2, 0)
        self.layout.addWidget(self.eraser_size_dropdown, 2, 1)
        self.layout.addWidget(self.heading_default, 3, 0)
        self.layout.addWidget(self.heading_default_checkbox, 3, 1)
        self.layout.addWidget(self.save_btn, 4, 1)
        self.setLayout(self.layout)

    def update_pref(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        name_update = self.name_edit.text()
        config.set("DEFAULT", "name", name_update)
        self.name_updated.emit(name_update)
        pen_width = str(self.pen_size_dropdown.currentText())
        config.set("DEFAULT", "pen_size", pen_width)
        self.pen_width_updated.emit(int(pen_width))
        eraser_width = str(self.eraser_size_dropdown.currentText())
        self.eraser_width_updated.emit(int(eraser_width))
        config.set("DEFAULT", "eraser_size", eraser_width)
        if self.heading_default_checkbox.isChecked():
            config.set("DEFAULT", "name_heading", "True")
        else:
            config.set("DEFAULT", "name_heading", "False")
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)