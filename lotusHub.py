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

class UIHubWindow(QWidget):
    def __init__(self, parent=None):
        super(UIHubWindow, self).__init__(parent)

        ########### Lotus Text ###########
        self.layout = QtWidgets.QVBoxLayout()
        self.heading_text = QtWidgets.QLabel("LOTUS")
        self.heading_text.setFont(QtGui.QFont('Arial', 20))
        self.heading_text.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.heading_text)
        self.setLayout(self.layout)

        ########### Buttons ###########
        self.new_note_button = QPushButton("New Note", self)
        self.new_note_button.move(750, 480)

        ########### CSS Stylesheet (experimental) ###########
        self.setStyleSheet("""
                QLabel {
                        color: white;
                }
                QPushButton {
                    	background-color:#44c767;
                        border-radius:28px;
                        border:1px solid #18ab29;
                        color:#ffffff;
                        font-family:Arial;
                        font-size:17px;
                        text-decoration:none;
                    }
                QPushButton:hover {
                        background-color: #3db35c;
                }
                """)