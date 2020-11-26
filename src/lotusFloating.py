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
        self.setMinimumWidth(self.child_widget.width())
        self.setMinimumHeight(self.child_widget.height())
        self.setGeometry(50, 50, self.child_widget.width(), self.child_widget.height())

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: white; border:1px solid black;')
        self.mouse_move = False
        self.mouse_resize = False

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.width() - event.pos().x() < 10 or self.height() - event.pos().y() < 10:
                self.mouse_resize = True
            elif event.pos().x() < 10 or event.pos().y() < 10:
                self.mouse_resize = True
                self.mouse_move = True
            else:
                self.mouse_move = True
        self.move_position = QtCore.QPoint(event.globalX() - self.geometry().x(), event.globalY() - self.geometry().y())
        self.resize_lr_position = QtCore.QPoint(event.globalX() - self.width(), event.globalY() - self.height())
        self.resize_ur_position = QtCore.QPoint(event.globalX() + self.width(), event.globalY() + self.height())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.mouse_resize and self.mouse_move:
            end_position = self.resize_ur_position - event.globalPos()
            self.resize(end_position.x(), end_position.y())
            end_position = event.globalPos() - self.move_position
            self.move(end_position)
        elif self.mouse_move:
            end_position = event.globalPos() - self.move_position
            self.move(end_position)
        elif self.mouse_resize:
            end_position = event.globalPos() - self.resize_lr_position # QGlobal - GGlobal + width
            self.resize(end_position.x(), end_position.y())

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.mouse_move = False
        self.mouse_resize = False




