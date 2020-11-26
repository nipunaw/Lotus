# CIS 4930
########### Contributors ###########
# Nipuna Weerapperuma
# Hannah Williams
# David Jaworski
# Carlos Morales-Diaz
# Spencer Bass

########### PyQT5 imports ###########
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class FloatingWidget(QtWidgets.QWidget):
    def __init__(self, child, parent):
        super().__init__(parent=parent)

        self.child_widget = child
        self.child_widget.setParent(self)

        self.position_x = self.pos().x()
        self.position_y = self.pos().y()
        self.width_container = 200
        self.height_container = 200
        self.setFixedWidth(400)
        self.setGeometry(50, 50, self.width_container, self.height_container)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: white; border:1px solid black;')

        #print(self.geometry())
        #self.setStyleSheet("background-color: red; border: 1px solid black")
        self.move = False
        #print(self.child_widget.geometry())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self.position_x < event.pos().x() < self.width_container - self.position_x and self.position_y < event.pos().y() < self.height_container - self.position_y:
            print("lit")
            self.move = True
            self.mouse_position = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.move:
            self.position_x = self.position_x + event.pos().x()-self.mouse_position.x()
            self.position_y = self.position_y + event.pos().y() - self.mouse_position.y()
            self.setGeometry(self.position_x, self.position_y , 200, 200)
            self.mouse_position = event.pos()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.move = False




