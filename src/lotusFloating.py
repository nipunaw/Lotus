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
        self.setMinimumWidth(self.child_widget.width()+6)
        self.setMinimumHeight(self.child_widget.height()+6)
        self.setGeometry(50, 50, self.child_widget.width()+6, self.child_widget.height()+6)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.child_widget.move(3, 3)
        self.child_widget.setStyleSheet('border-width: 0px 0px 0px 0px;')
        self.setStyleSheet('background-color: white; border:1px solid black;')

        self.move_only = False
        self.left_side = False
        self.right_side = False
        self.top_side = False
        self.bottom_side = False



        ## Right-click options
        self.menu = QtWidgets.QMenu(self)
        deleteAction = QtWidgets.QAction('Delete', self)
        deleteAction.triggered.connect(self.deleteLater)
        self.menu.addAction(deleteAction)

        ## Cursor
        self.setMouseTracking(True)
        self.child_widget.setMouseTracking(True)
        self.curr_cursor_shape = QtGui.QCursor().shape()
        self.cursor = QtGui.QCursor()
        self.installEventFilter(self)

    def leaveEvent(self, event):
       self.cursor.setShape(self.curr_cursor_shape)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if event.pos().x() < 10:
                self.left_side = True
            if event.pos().y() < 10:
                self.top_side = True
            if self.width() - event.pos().x() < 10:
                self.right_side = True
            if self.height() - event.pos().y() < 10:
                self.bottom_side = True
            if not (self.left_side or self.top_side or self.right_side or self.bottom_side):
                self.move_only = True

        self.start_size = QtCore.QPoint(self.width(), self.height())
        self.start_geometry = QtCore.QPoint(self.geometry().x(), self.geometry().y())
        self.start_mouse_position = event.globalPos()

        if event.button() == Qt.RightButton:
            self.menu.popup(QtGui.QCursor.pos())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        #print(('Mouse coords: ( %d : %d )' % (event.x(), event.y())))
        self.curr_cursor_shape = QtGui.QCursor().shape() ## Setting cursor
        if event.pos().x() < 10 and event.pos().y() < 10:
            self.cursor.setShape(Qt.SizeFDiagCursor)
        elif self.width() - event.pos().x() < 10 and event.pos().y() < 10:
            self.cursor.setShape(Qt.SizeBDiagCursor)
        elif self.width() - event.pos().x() < 10 and self.height() - event.pos().y() < 10:
            self.cursor.setShape(Qt.SizeFDiagCursor)
        elif event.pos().x() < 10 and self.height() - event.pos().y() < 10:
            self.cursor.setShape(Qt.SizeBDiagCursor)
        elif event.pos().x() < 10:
            self.cursor.setShape(Qt.SizeHorCursor)
        elif event.pos().y() < 10:
            self.cursor.setShape(Qt.SizeVerCursor)
        elif self.width() - event.pos().x() < 10:
            self.cursor.setShape(Qt.SizeHorCursor)
        elif self.height() - event.pos().y() < 10:
            self.cursor.setShape(Qt.SizeVerCursor)
        else:
            self.cursor.setShape(Qt.ArrowCursor)
        self.setCursor(self.cursor)

        if self.move_only:
            self.move(event.globalPos() - self.start_mouse_position + self.start_geometry)
        elif self.left_side and self.top_side: # upper left corner
            resize_point = self.start_mouse_position - event.globalPos() + self.start_size
            self.resize(resize_point.x(), resize_point.y())
            self.move(event.globalPos() - self.start_mouse_position + self.start_geometry)
        elif self.right_side and self.top_side: # upper right corner
            resize_point = self.start_mouse_position - event.globalPos() + self.start_size
            resize_point_inverted = event.globalPos() - self.start_mouse_position + self.start_size
            self.resize(resize_point_inverted.x(), resize_point.y())
            self.move(self.start_geometry.x(), event.globalY() - self.start_mouse_position.y() + self.start_geometry.y())
        elif self.left_side and self.bottom_side: # lower left corner
            resize_point = self.start_mouse_position - event.globalPos() + self.start_size
            resize_point_inverted = event.globalPos() - self.start_mouse_position + self.start_size
            self.resize(resize_point.x(), resize_point_inverted.y())
            self.move(event.globalX() - self.start_mouse_position.x() + self.start_geometry.x(), self.start_geometry.y())
        elif self.right_side and self.bottom_side: # lower right corner
            resize_point_inverted = event.globalPos() - self.start_mouse_position + self.start_size
            self.resize(resize_point_inverted.x(), resize_point_inverted.y())
        elif self.left_side: # left side
            resize_point = self.start_mouse_position - event.globalPos() + self.start_size
            self.resize(resize_point.x(), self.start_size.y())
            self.move(event.globalX() - self.start_mouse_position.x() + self.start_geometry.x(), self.start_geometry.y())
        elif self.right_side: # right side
            resize_point_inverted = event.globalPos() - self.start_mouse_position + self.start_size
            self.resize(resize_point_inverted.x(), self.start_size.y())
        elif self.top_side: # top side
            resize_point = self.start_mouse_position - event.globalPos() + self.start_size
            self.resize(self.start_size.x(), resize_point.y())
            self.move(self.start_geometry.x(), event.globalY() - self.start_mouse_position.y() + self.start_geometry.y())
        elif self.bottom_side: # bottom side
            resize_point_inverted = event.globalPos() - self.start_mouse_position + self.start_size
            self.resize(self.start_size.x(), resize_point_inverted.y())
        self.child_widget.resize(self.width() - 6, self.height() - 6)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.move_only = False
        self.left_side = False
        self.right_side = False
        self.top_side = False
        self.bottom_side = False




