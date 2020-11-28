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
from enum import Enum
import pytesseract
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPoint, QRect
from PyQt5.QtGui import QRegion, QColor, QPainter, QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QMessageBox, QScrollArea, QGridLayout, QHBoxLayout, \
    QVBoxLayout, QSizePolicy, QAction

from src.constants import CONFIG_FILE, DIRECTORY_FILE, SCHEDULE_FILE_PATH, SCHEDULED_NOTES_DIRECTORY, assets
from src.lotusButtons import ToolButton
from src.lotusFloating import FloatingWidget

def default_config():
    os.makedirs(SCHEDULED_NOTES_DIRECTORY, exist_ok=True)
    try:
        file = open(CONFIG_FILE, 'r')
    except IOError:
        file = open(CONFIG_FILE, 'w')
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'Name': '',
                             'Pen_Size': '5',
                             'Eraser_Size': '5',
                             'Name_Heading': 'True'}
        config.write(file)
    file.close()

def pen_size():
    default_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return int(config['DEFAULT']['pen_size'])

def eraser_size():
    default_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return int(config['DEFAULT']['eraser_size'])

def highlighter_size():
    return 30

def set_default_pen_width(width):
    Utensils.PEN.radius = width

def set_default_eraser_width(width):
    Utensils.ERASER.radius = width

class Utensil:
    def __init__(self, color : QColor, radius : int,
                 brush_style : Qt.PenStyle = Qt.SolidLine,
                 cap_style : Qt.PenCapStyle = Qt.RoundCap,
                 join_style : Qt.PenJoinStyle = Qt.RoundJoin,
                 fill_style : Qt.BrushStyle = Qt.SolidPattern):
        self.maxWidth = 32
        self.minWidth = 5
        self.color = color
        self.radius = radius
        self.brush_style = brush_style
        self.fill_style = fill_style
        self.cap_style = cap_style
        self.join_style = join_style

    def incrementWidth(self):
        result = self.radius + 1
        self.radius = result if result < self.maxWidth else self.maxWidth

    def decrementWidth(self):
        result = self.radius - 1
        self.radius = result if result >= self.minWidth else self.minWidth

    def pen(self):
        pen = QtGui.QPen()
        pen.setStyle(self.brush_style)
        pen.setWidth(self.radius)
        pen.setColor(self.color)
        pen.setCapStyle(self.cap_style)
        pen.setJoinStyle(self.join_style)
        return pen

    def highlighter(self):
        highlighter = QtGui.QBrush()
        highlighter.setStyle(self.fill_style)
        highlighter.setColor(self.color)
        return highlighter

class Utensils(Utensil, Enum):
    PEN = (Qt.black, pen_size())
    ERASER = (Qt.white, eraser_size())
    HIGHLIGHTER = (QColor(248, 222, 126, 80), highlighter_size(), Qt.NoPen, Qt.SquareCap, Qt.MiterJoin, Qt.SolidPattern)

class Canvas(QLabel):
    layer_change = pyqtSignal()
    scrolled = pyqtSignal(QtGui.QWheelEvent)
    mouse_grab = pyqtSignal(QPoint)
    def __init__(self):
        super(Canvas, self).__init__()
        self.setStyleSheet("background-color: black")
        master_canvas_layer = QtGui.QPixmap(self.size())
        master_canvas_layer.fill(Qt.white)
        self.activeLayers = []
        self.activeLayers.append(master_canvas_layer)
        self.inactiveLayers = []
        self.floatingWidgets = []
        #self.canvasLayers = [master_canvas_layer] # Deprecated
        #self.activeLayers = [True] # Deprecated
        # self.numLayers = 1 # Deprecated
        # self.activePointer = 1 # Deprecated
        self.last_save = None
        self.setPixmap(self.activeLayers[0])
        ########### Writing parameters ###########
        # General utensil parameters
        self.utensil_press = False
        self.current_utensil = Utensils.PEN
        # Scrolling Parameters
        self.mouse_button_scrolling = False
        # Pen default parameters
        self.pen_lastPoint = QtCore.QPoint()
        # Eraser default parameters
        self.eraser_lastPoint = QtCore.QPoint()
        self.cursor_update()
        #self.cursor_pix_scaled = QPixmap(assets["pen_eraser_cursor"]).scaled(QSize(self.current_utensil.radius, self.current_utensil.radius), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #self.cursor = QtGui.QCursor(self.cursor_pix_scaled)
        #self.cursor.setShape(Qt.CrossCursor)
        #self.setCursor(self.cursor)
        # Drawing path
        self.drawing_path_layers = []
        #self.drawing_path = QtGui.QPainterPath()

        self.tableWidget = QLabel("Hello")
        self.tableWidget.setGeometry(0, 0, 200, 200)
        self.test_2 = FloatingWidget(self.tableWidget, self, 20, 20)
        self.floatingWidgets.append(self.test_2)

        self.helloWidget = QtWidgets.QLineEdit()
        self.helloWidget.setGeometry(0, 0, 200, 100)
        self.test_3 = FloatingWidget(self.helloWidget, self, 10, 10)
        self.test_3.setGeometry(10, 10, 300, 200)
        self.floatingWidgets.append(self.test_3)

        # Painters
        self.painter = QPainter()
        self.layer_painter = QPainter()

    def cursor_update(self):
        if not self.current_utensil == Utensils.HIGHLIGHTER:
            cursor_pixmap = QPixmap(assets["pen_eraser_cursor"]).scaled(QSize(self.current_utensil.radius, self.current_utensil.radius), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            cursor = QtGui.QCursor(cursor_pixmap)
            self.setCursor(cursor)
        else:
            cursor = QtGui.QCursor()
            cursor.setShape(Qt.CrossCursor)
            self.setCursor(cursor)


    def resizeLayer(self, i, size, active=True):
        temp = self.activeLayers[i] if active else self.inactiveLayers[i]
        if temp.size() == size:
            return
        if active:
            self.activeLayers[i] = QtGui.QPixmap(size)
            self.activeLayers[i].fill(Qt.transparent if i != 0 else Qt.white)
            self.layer_painter.begin(self.activeLayers[i])
        else:
            temp = self.inactiveLayers[i]
            self.inactiveLayers[i] = QtGui.QPixmap(size)
            self.inactiveLayers[i].fill(Qt.transparent)
            self.layer_painter.begin(self.inactiveLayers[i])
        self.layer_painter.drawPixmap(temp.rect(), temp, temp.rect())
        self.layer_painter.end()

    def resizeCanvas(self, size):
        temp = self.activeLayers[0]
        self.activeLayers[0] = QtGui.QPixmap(size)
        self.activeLayers[0].fill(Qt.white)
        self.painter = QtGui.QPainter(self.activeLayers[0])
        self.painter.drawPixmap(self.activeLayers[0].rect(), temp, temp.rect())
        self.painter.end()
        self.setPixmap(self.activeLayers[0])

        for i in range (0, len(self.activeLayers)):
            self.resizeLayer(i, self.size())

        if self.last_save is None:
            self.startSize = self.size()
            self.last_save = self.activeLayers[0].toImage()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if self.activeLayers[0].size() != self.size():
            self.resizeCanvas(self.size())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.utensil_press = True
            # self.numLayers += 1
            new_canvas_layer = QtGui.QPixmap(self.size())
            new_canvas_layer.fill(Qt.transparent)

            self.painter.begin(new_canvas_layer)
            self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
            self.painter.setPen(self.current_utensil.pen())
            self.painter.drawPoint(event.pos())

            self.activeLayers.append(new_canvas_layer)
            self.inactiveLayers.clear()

            self.layer_change.emit()

            self.last_point_draw = event.pos()
            self.update()
            self.painter.end()
        elif event.button() == Qt.MiddleButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.last_point_scroll = event.globalPos()
            self.mouse_button_scrolling = True
        else:
            super(Canvas, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() and Qt.LeftButton and self.utensil_press:
            x = self.width() - event.pos().x()
            y = self.height() - event.pos().y()
            if x < 200:
                if y < 200:
                    self.resizeLayer(-1, QSize(self.width() + 100, self.height() + 100))
                    self.resizeCanvas(QSize(self.width() + 100, self.height()))
                else:
                    self.resizeLayer(-1, QSize(self.width() + 100, self.height()))
                    self.resizeCanvas(QSize(self.width() + 100, self.height()))
            elif y < 200:
                self.resizeLayer(-1, QSize(self.width(), self.height() + 100))
                self.resizeCanvas(QSize(self.width(), self.height() + 100))
            self.painter.begin(self.activeLayers[len(self.activeLayers) - 1])
            self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
            self.painter.setPen(self.current_utensil.pen())
            if not self.current_utensil == Utensils.HIGHLIGHTER:
                self.painter.drawLine(self.last_point_draw, event.pos())
                self.last_point_draw = event.pos()
            self.update()
            self.painter.end()
        elif event.buttons() and Qt.MiddleButton and self.mouse_button_scrolling:
            offset = self.last_point_scroll - event.globalPos()
            self.last_point_scroll = event.globalPos()
            self.mouse_grab.emit(offset)
        else:
            super(Canvas, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.current_utensil == Utensils.HIGHLIGHTER:
                self.painter.begin(self.activeLayers[len(self.activeLayers) - 1])
                self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
                self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
                self.painter.setPen(self.current_utensil.pen())
                self.painter.setBrush(self.current_utensil.highlighter())
                self.painter.drawRect(self.last_point_draw.x(), self.last_point_draw.y(), (event.pos().x() -self.last_point_draw.x()), (event.pos().y() -self.last_point_draw.y()))
                self.update()
                self.painter.end()
            self.utensil_press = False

        elif event.button() == Qt.MiddleButton:
            self.setCursor(self.cursor)
            self.mouse_button_scrolling = False


    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if event.button() == Qt.LeftButton:
    #         self.utensil_press = True
    #         # self.numLayers += 1
    #         new_canvas_layer = QtGui.QPixmap(self.size())
    #         new_canvas_layer.fill(Qt.transparent)
    #
    #         #self.painter.begin(new_canvas_layer)
    #         #self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    #         #self.painter.setPen(self.current_utensil.pen())
    #
    #         #self.drawing_path_part = QtGui.QPainterPath()
    #         # drawing_path = QtGui.QPainterPath()
    #         # drawing_path.moveTo(event.pos())
    #         self.drawing_path_part = QtGui.QPainterPath()
    #         self.drawing_path_part.moveTo(event.pos())
    #         # self.drawing_path_layers.append(drawing_path)
    #
    #         #self.painter.drawPoint(event.pos())
    #
    #         self.activeLayers.append(new_canvas_layer)
    #         self.last_point_draw = event.pos()
    #         self.update()
    #         # self.painter.end()
    #     elif event.button() == Qt.MiddleButton:
    #         self.setCursor(Qt.ClosedHandCursor)
    #         self.last_point_scroll = event.globalPos()
    #         self.mouse_button_scrolling = True
    #     else:
    #         super(Canvas, self).mousePressEvent(event)
    #
    # def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if event.buttons() and Qt.LeftButton and self.utensil_press:
    #         x = self.width() - event.pos().x()
    #         y = self.height() - event.pos().y()
    #         if x < 200:
    #             if y < 200:
    #                 self.resizeLayer(-1, QSize(self.width() + 100, self.height() + 100))
    #                 self.resizeCanvas(QSize(self.width() + 100, self.height()))
    #             else:
    #                 self.resizeLayer(-1, QSize(self.width() + 100, self.height()))
    #                 self.resizeCanvas(QSize(self.width() + 100, self.height()))
    #         elif y < 200:
    #             self.resizeLayer(-1, QSize(self.width(), self.height() + 100))
    #             self.resizeCanvas(QSize(self.width(), self.height() + 100))
    #         #self.painter.begin(self.activeLayers[len(self.activeLayers) - 1])
    #         #self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    #
    #         #self.painter.setPen(self.current_utensil.pen())
    #         # self.painter.drawLine(self.last_point_draw, event.pos())
    #         #self.drawing_path_part.closeSubpath()
    #         self.drawing_path_part.lineTo(event.pos())
    #         self.painter.begin(self.activeLayers[len(self.activeLayers) - 1])
    #         #self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    #         self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    #         self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
    #         self.painter.setPen(self.current_utensil.pen())
    #         #self.drawing_path_layers[len(self.drawing_path_layers)-1].addPath(self.drawing_path_part)
    #         self.painter.drawPath(self.drawing_path_part) #self.drawing_path_layers[len(self.drawing_path_layers)-1]
    #         #self.drawing_path_part.moveTo(event.pos())
    #         # self.drawingPath = None
    #         self.update()
    #         self.painter.end()
    #
    #         # self.last_point_draw = event.pos()
    #         # self.update()
    #         #self.painter.end()
    #     elif event.buttons() and Qt.MiddleButton and self.mouse_button_scrolling:
    #         offset = self.last_point_scroll - event.globalPos()
    #         self.last_point_scroll = event.globalPos()
    #         self.mouse_grab.emit(offset)
    #     else:
    #         super(Canvas, self).mouseMoveEvent(event)
    #
    # def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if event.button() == Qt.LeftButton:
    #         self.utensil_press = False
    #         # self.painter.begin(self.activeLayers[len(self.activeLayers) - 1])
    #         # self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    #         # self.painter.setPen(self.current_utensil.pen())
    #         # self.painter.drawPath(self.drawingPath)
    #         # #self.drawingPath = None
    #         # self.update()
    #         # self.painter.end()
    #     elif event.button() == Qt.MiddleButton:
    #         self.setCursor(self.cursor)
    #         self.mouse_button_scrolling = False

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.scrolled.emit(event)

    def paintEvent(self, event):
        #self.activeLayers[0].fill(Qt.white)
        self.layer_painter.begin(self.activeLayers[0])
        self.layer_painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.layer_painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        #print(len(self.activeLayers))
        self.layer_painter.drawPixmap(self.activeLayers[0].rect(), self.activeLayers[len(self.activeLayers)-1])
        #for i in range(1, len(self.activeLayers)):
        #    self.layer_painter.drawPixmap(self.activeLayers[0].rect(), self.activeLayers[i])
        self.layer_painter.end()
        self.setPixmap(self.activeLayers[0])
        super(Canvas, self).paintEvent(event)

    # def paintEvent(self, event):
    #     self.activeLayers[0].fill(Qt.white)
    #     self.layer_painter.begin(self.activeLayers[0])
    #     self.layer_painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    #     self.layer_painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
    #     for i in range(1, len(self.activeLayers)):
    #         self.layer_painter.drawPixmap(self.activeLayers[0].rect(), self.activeLayers[i])
    #     self.layer_painter.end()
    #     self.setPixmap(self.activeLayers[0])
    #     super(Canvas, self).paintEvent(event)

    def hasChanged(self):
        if self.last_save is None:
            return False
        return not self.pixmap().toImage() == self.last_save

    def floatingWidgetPlace(self, widget):
        new_floating_canvas_layer = QtGui.QPixmap(self.size())
        new_floating_canvas_layer.fill(Qt.transparent)
        self.painter.begin(new_floating_canvas_layer)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        self.painter.drawPixmap(widget.geometry().x(), widget.geometry().y(), widget.grab())
        self.activeLayers.append(new_floating_canvas_layer)
        self.painter.end()
        self.update()
        widget.deleteLater()
        self.floatingWidgets.remove(widget)
        self.layer_change.emit()

    def save(self, file_path):
        # for i in self.floatingWidgets: ## TODO: Save un-placed floating widgets
        #     self.floatingWidgetPlace(i)
        self.activeLayers[0].save(file_path)
        self.last_save = self.activeLayers[0].toImage()

    def setUtensil(self, utensil : Utensil):
        self.current_utensil = utensil

    # Button click handling
    def clear(self):
        # Reset canvas
        clear_canvas_layer = QtGui.QPixmap(self.size())
        clear_canvas_layer.fill(Qt.white)
        self.activeLayers.append(clear_canvas_layer)
        self.update()
        self.resizeCanvas(self.startSize)
        # Reset back to pen tool (done outside)
        # self.setUtensil(Utensils.PEN)

    def change_master_layer(self):
        self.activeLayers[0].fill(Qt.white)
        self.layer_painter.begin(self.activeLayers[0])
        self.layer_painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.layer_painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        for i in range(1, len(self.activeLayers)):
            self.layer_painter.drawPixmap(self.activeLayers[0].rect(), self.activeLayers[i])
        self.layer_painter.end()
        self.setPixmap(self.activeLayers[0])


    def undo(self):
        if len(self.activeLayers) > 1:
            #self.activeLayers[0] = self.activeLayers[0] or self.activeLayers[len(self.activeLayers) - 1]
            #mask = self.activeLayers[len(self.activeLayers) - 1].createMaskFromColor()

            # self.layer_painter.begin(self.activeLayers[0])
            # self.layer_painter.setCompositionMode(QPainter.RasterOp_SourceXorDestination)
            # self.layer_painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            # self.layer_painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
            # self.layer_painter.drawPixmap(self.activeLayers[0].rect(), self.activeLayers[len(self.activeLayers) - 1])
            # #self.layer_painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            # self.layer_painter.end()
            # self.setPixmap(self.activeLayers[0])

            #self.update()
            #self.activeLayers[0].begin(self.activeLayers[0])

            self.inactiveLayers.append(self.activeLayers.pop())
            self.change_master_layer()
            self.layer_change.emit()
        #self.update()

    def redo(self): # Now finishing command pattern
        if len(self.inactiveLayers) > 0:
            self.activeLayers.append(self.inactiveLayers.pop())
            self.update()
            self.layer_change.emit()
        #self.update()

    def loadImage(self, file_path):
        image_pixmap = QtGui.QPixmap(file_path)
        canvas = QtGui.QPixmap(self.minimumSize().expandedTo(image_pixmap.size()))
        blank = QtGui.QPixmap(canvas.size())
        blank.fill(Qt.white)
        self.activeLayers = [blank, canvas]
        self.inactiveLayers.clear()
        self.painter.begin(canvas)
        self.painter.drawPixmap(canvas.rect(), image_pixmap, image_pixmap.rect())
        self.painter.end()
        self.resizeCanvas(self.activeLayers[0].size())
        self.update()
        self.last_save = self.activeLayers[0].toImage()

class CanvasWindow(QScrollArea):
    def __init__(self):
        super(CanvasWindow, self).__init__()
        self.setWidgetResizable(True)
        self.layout = QVBoxLayout()
        self.label = Canvas()
        self.label.scrolled.connect(self.scrollForLabel)
        self.label.mouse_grab.connect(self.mouseGrabScroll)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.label, Qt.AlignTop | Qt.AlignLeft)

        self.setWidget(self.label)
        self.setLayout(self.layout)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def mouseGrabScroll(self, offset):
        x = self.horizontalScrollBar().value() + offset.x()
        y = self.verticalScrollBar().value() + offset.y()
        self.horizontalScrollBar().setValue(x)
        self.verticalScrollBar().setValue(y)

    def scrollForLabel(self, event: QtGui.QWheelEvent):
        hval = self.horizontalScrollBar().value()
        vval = self.verticalScrollBar().value()
        newx = hval - (event.angleDelta().x() / (8 * 15)) * self.horizontalScrollBar().singleStep()
        newy = vval - (event.angleDelta().y() / (8 * 15)) * self.verticalScrollBar().singleStep()
        hmin = self.horizontalScrollBar().minimum()
        hmax = self.horizontalScrollBar().maximum()
        if hmin < newx < hmax:
            self.horizontalScrollBar().setValue(newx)
        elif hmin >= newx:
            self.horizontalScrollBar().setValue(hmin)
        elif hmax <= newx:
            self.horizontalScrollBar().setValue(hmax)
        ymin = self.verticalScrollBar().minimum()
        ymax = self.verticalScrollBar().maximum()
        if ymin < newy < ymax:
            self.verticalScrollBar().setValue(newy)
        elif ymin >= newy:
            self.verticalScrollBar().setValue(ymin)
        elif ymax <= newy:
            self.verticalScrollBar().setValue(ymax)

class UINoteWindow(QWidget):
    deleted_file = pyqtSignal(str)

    def __init__(self, file_path:str, parent=None, scheduled=False):
        super(UINoteWindow, self).__init__(parent)

        self.file_path = file_path
        self.scheduled = scheduled

        ########### Menu Bar ###########
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("File")

        # Open
        self.open_option = QtWidgets.QAction("Open", self)
        self.open_option.setShortcut("Ctrl+O")
        self.open_option.triggered.connect(lambda state: self.open())
        self.file_menu.addAction(self.open_option)

        self.open_recent_option = QtWidgets.QMenu("Open Recent", self)

        self.file_menu.addMenu(self.open_recent_option)
        if not self.update_open_recent_menu():
            self.open_recent_option.setDisabled(True)

        # Headings
        self.heading_option = QtWidgets.QAction("Add/Edit Heading", self)
        self.heading_option.setShortcut("Ctrl+H")
        self.heading_option.triggered.connect(self.heading)
        self.template_menu = self.menu_bar.addMenu("Template")
        self.template_menu.addAction(self.heading_option)

        self.settings_option = QtWidgets.QAction("Font")
        self.settings_option.triggered.connect(self.settings)
        self.settings_menu = self.menu_bar.addMenu("Settings")
        self.settings_menu.addAction(self.settings_option)

        # Saving
        self.save_option = QtWidgets.QAction("Save", self)
        self.save_option.setShortcut("Ctrl+S")
        self.save_option.triggered.connect(self.save)
        self.file_menu.addAction(self.save_option)

        self.save_as_option = QtWidgets.QAction("Save As" if not scheduled else "Export", self)
        self.save_as_option.setShortcut("F12")
        self.save_as_option.triggered.connect(self.save_as)
        self.file_menu.addAction(self.save_as_option)

        # OCR
        self.find_ocr = QtWidgets.QAction("Find Typed/Neat Text", self)
        self.find_ocr.triggered.connect(self.ocr)
        self.ocr_menu = self.menu_bar.addMenu("OCR")
        self.ocr_menu.addAction(self.find_ocr)

        ########### Buttons ###########
        # Handled by resizeEvent
        self.heading_font = QtGui.QFont("Times New Roman", 10, QtGui.QFont.Bold)
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        name = config['DEFAULT']['name']
        self.heading_title = QtWidgets.QLineEdit()
        self.heading_name = QtWidgets.QLineEdit(name)
        self.heading_course = QtWidgets.QLineEdit()
        self.heading_date = QtWidgets.QLineEdit()
        self.add_date = True

        ########### Layout ############
        self.setMinimumSize(1200, 600)
        self.canvas_window = CanvasWindow()
        self.canvas_window.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layout = QVBoxLayout()

        # self.heading_title = QtWidgets.QLineEdit()
        # title_font = QtGui.QFont("Times New Roman", 20)
        # self.heading_title.setFont(title_font)
        # self.heading_title.setStyleSheet("border: 0px")
        # self.layout.addWidget(self.heading_title)
        #
        # subheading_font = QtGui.QFont("Times New Roman", 15)
        # self.heading_name = QtWidgets.QLineEdit()
        # self.heading_name.setFont(subheading_font)
        # self.heading_name.setStyleSheet("border: 0px")
        # self.layout.addWidget(self.heading_name)
        #
        # self.heading_course = QtWidgets.QLineEdit()
        # self.heading_course.setFont(subheading_font)
        # self.heading_course.setStyleSheet("border: 0px")
        # self.layout.addWidget(self.heading_course)
        #
        # self.heading_date = QtWidgets.QLineEdit()
        # self.heading_date.setFont(subheading_font)
        # self.heading_date.setStyleSheet("border: 0px")
        # self.layout.addWidget(self.heading_date)

        self.header_text = QtWidgets.QPlainTextEdit()
        self.header_widget = FloatingWidget(self.header_text, self.canvas_window.label)
        self.header_widget.hide()

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.canvas_window, Qt.AlignTop)
        self.button_container = QtWidgets.QFrame()
        #self.button_toolbar = QtWidgets.QToolBar(self.button_container)
        self.button_layout = QGridLayout(self.button_container)
        self.button_layout.setContentsMargins(10,10,10,10)

        self.tool_buttons_ui()
        self.button_layout_ui()
        self.layout.addWidget(self.button_container, Qt.AlignBottom)
        self.setLayout(self.layout)
        self.layout.setMenuBar(self.menu_bar)

        # Layer Management
        self.canvas_window.label.layer_change.connect(self.change_layers)

        ########### Saving/Opening ###########
        if self.scheduled:
            self.open_directory(self.file_path)
        elif self.file_path is not None:
            self.file_path = self.file_path[:-1]
            self.open_directory(self.file_path)
        else:
            self.file_path = ""

        self.file_path_2 = ""

    ########### Closing ###########
    def closeEvent(self, event):
        if self.canvas_window.label.hasChanged():
            self.savePopup()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_BracketLeft:
            self.canvas_window.label.current_utensil.decrementWidth()
            #for u in Utensils:
            #    u.decrementWidth()
            self.canvas_window.label.cursor_update()
        elif event.key() == Qt.Key_BracketRight:
            self.canvas_window.label.current_utensil.incrementWidth()
            #for u in Utensils:
            #    u.incrementWidth()
            self.canvas_window.label.cursor_update()

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

    def erase(self):
        self.canvas_window.label.setUtensil(Utensils.ERASER)
        self.canvas_window.label.cursor_update()
        self.color_indicator_update()
        self.eraser_button.setEnabled(False)
        self.highlighter_button.setEnabled(True)
        self.pen_button.setEnabled(True)

    def pen(self):
        self.canvas_window.label.setUtensil(Utensils.PEN)
        self.canvas_window.label.cursor_update()
        self.color_indicator_update()
        self.pen_button.setEnabled(False)
        self.highlighter_button.setEnabled(True)
        self.eraser_button.setEnabled(True)

    def highlight(self):
        self.canvas_window.label.setUtensil(Utensils.HIGHLIGHTER)
        self.canvas_window.label.cursor_update()
        self.color_indicator_update()
        self.highlighter_button.setEnabled(False)
        self.pen_button.setEnabled(True)
        self.eraser_button.setEnabled(True)

    def button_layout_ui(self):
        self.button_container.setStyleSheet("background-color: #e1e1e1; border-radius: 30px;")
        self.button_container.setFixedHeight(60)

    # def home_button_display(self):
    #     self.home_button = QPushButton('Toggle home', self)
    #     self.button_layout.addWidget(self.home_button, 0, 5)
    #     self.home_button.setToolTip("Clear any writing")
    #
    # def clear_button_display(self):
    #     self.clear_button = QtWidgets.QPushButton("Clear All", self)
    #     self.button_layout.addWidget(self.clear_button, 0, 3)
    #     self.clear_button.setToolTip("Clear any writing")
    #     self.clear_button.clicked.connect(self.canvas_window.label.clear)
    #     self.clear_button.clicked.connect(self.pen)
    #
    # def eraser_button_display(self):
    #     self.eraser_button = QtWidgets.QPushButton("Eraser", self)
    #     self.eraser_button.setDisabled(False)
    #     self.button_layout.addWidget(self.eraser_button, 0, 1)
    #     self.eraser_button.setToolTip("Erase any writing")
    #     self.eraser_button.clicked.connect(self.erase)

    def tool_buttons_ui(self):
        self.pen_button = ToolButton(assets["pen"])
        self.button_layout.addWidget(self.pen_button, 0, 0)
        self.pen_button.clicked.connect(self.pen)
        self.eraser_button = ToolButton(assets["eraser"])
        self.button_layout.addWidget(self.eraser_button, 0, 1)
        self.eraser_button.clicked.connect(self.erase)
        self.highlighter_button = ToolButton(assets["highlighter"])
        self.button_layout.addWidget(self.highlighter_button, 0, 2)
        self.highlighter_button.clicked.connect(self.highlight)
        self.color_indicator = ToolButton(assets["color_indicator"], 35, 35)
        self.button_layout.addWidget(self.color_indicator, 0, 3)
        self.color_indicator_update()
        self.color_button = ToolButton(assets["color_wheel"])
        self.button_layout.addWidget(self.color_button, 0, 3)
        self.color_button.clicked.connect(self.color_selector)
        self.undo_button = ToolButton(assets["undo"])
        self.undo_button.setDisabled(True)
        self.button_layout.addWidget(self.undo_button, 0, 4)
        self.undo_button.clicked.connect(self.canvas_window.label.undo)
        self.redo_button = ToolButton(assets["redo"])
        self.redo_button.setDisabled(True)
        self.button_layout.addWidget(self.redo_button, 0, 5)
        self.redo_button.clicked.connect(self.canvas_window.label.redo)
        self.clear_button = ToolButton(assets["clear"])
        self.clear_button.setDisabled(True)
        self.button_layout.addWidget(self.clear_button, 0, 6)
        self.clear_button.clicked.connect(self.canvas_window.label.clear)
        self.clear_button.clicked.connect(self.pen)
        self.home_button  = ToolButton(assets["home"])
        self.button_layout.addWidget(self.home_button, 0, 7)
        #self.button_toolbar.setIconSize(QSize(48, 58))
        #self.button_toolbar.setStyleSheet("QToolBar {spacing: 17px;}")
        self.pen()

    def color_selector(self):
        color_dialog = QtWidgets.QColorDialog()
        color = color_dialog.getColor(self.canvas_window.label.current_utensil.color)

        if color.isValid():
            if self.canvas_window.label.current_utensil == Utensils.PEN:
                Utensils.PEN.color = color
            elif self.canvas_window.label.current_utensil == Utensils.HIGHLIGHTER:
                Utensils.HIGHLIGHTER.color = QColor(color.getRgb()[0], color.getRgb()[1], color.getRgb()[2], 80)
            self.color_indicator_update()
        #self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())

    def color_indicator_update(self):
        r = QColor(self.canvas_window.label.current_utensil.color).getRgb()[0]
        g = QColor(self.canvas_window.label.current_utensil.color).getRgb()[1]
        b = QColor(self.canvas_window.label.current_utensil.color).getRgb()[2]
        a = QColor(self.canvas_window.label.current_utensil.color).getRgb()[3]
        self.color_indicator.setStyleSheet("background-color: rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(a) + "); margin-top: 10px; margin-left: 10px;")

    def change_layers(self):
        if len(self.canvas_window.label.activeLayers) > 1:
            self.undo_button.setEnabled(True)
            self.clear_button.setEnabled(True)
        else:
            self.undo_button.setDisabled(True)
            self.clear_button.setDisabled(True)

        if len(self.canvas_window.label.inactiveLayers) > 0:
            self.redo_button.setEnabled(True)
        else:
            self.redo_button.setDisabled(True)


    # def pen_button_display(self):
    #     self.pen_button = ToolButton(assets["pen"])
    #
    #     # self.pen_button = QtWidgets.QPushButton("Pen", self)
    #     # self.pen_button.setDisabled(True) # In use by default
    #     # self.pen_button.resize(100, 32)
    #     self.button_layout.addWidget(self.pen_button, 0, 0)
    #     # self.pen_button.setToolTip("Premiere writing utensil")
    #     # self.pen_button.setStyleSheet("background-image: url(assets/Pen.png);")
    #     self.pen_button.clicked.connect(self.pen)
    #
    # def highlighter_button_display(self):
    #     self.highlighter_button = QtWidgets.QPushButton("Highlighter", self)
    #     self.highlighter_button.setDisabled(False)
    #     self.highlighter_button.resize(100, 32)
    #     self.button_layout.addWidget(self.highlighter_button, 0, 2)
    #     self.highlighter_button.setToolTip("Highlight any writing")
    #     self.highlighter_button.clicked.connect(self.highlight)
    #
    # def undo_button_display(self):
    #     self.undo_button = QtWidgets.QPushButton("Undo", self)
    #     self.undo_button.setDisabled(False)  # In use by default
    #     self.undo_button.resize(100, 32)
    #     self.button_layout.addWidget(self.undo_button, 0, 5)
    #     #self.undo_button.setToolTip("Premiere writing utensil")
    #     self.undo_button.clicked.connect(self.canvas_window.label.undo)
    #
    # def redo_button_display(self):
    #     self.redo_button = QtWidgets.QPushButton("Redo", self)
    #     self.redo_button.setDisabled(False)  # In use by default
    #     self.redo_button.resize(100, 32)
    #     self.button_layout.addWidget(self.redo_button, 0, 6)
    #     #self.redo_button.setToolTip("Premiere writing utensil")
    #     self.redo_button.clicked.connect(self.canvas_window.label.redo)

    ########### Saving ###########
    def save(self):
        if self.file_path == "":
            self.save_as()
        else:
            self.canvas_window.label.save(self.file_path)
            self.directories_update()
            self.update_open_recent_menu()
        self.update_open_recent_menu()

    def save_as(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                    "Save Notes", # Caption
                                                                    "notes.jpg", # File-name, directory
                                                                    "JPG (*.jpg);;PNG (*.png)") # File types

        # Blank file path
        if file_path == "":
            return
        self.file_path = file_path

        # Saving canvas
        self.canvas_window.label.save(self.file_path)
        self.directories_update()
        self.update_open_recent_menu()
        self.setWindowTitle(self.file_path)

    def directories_update(self):
        try:
            #file exists
            with open(DIRECTORY_FILE, "r") as f:
                paths = f.read().splitlines()
            #count = len(paths)
            if self.file_path in paths:
                paths.remove(self.file_path)
                paths.insert(0, self.file_path)
                with open(DIRECTORY_FILE, "w") as f:
                    f.writelines(p + "\n" for p in paths)
            else:
                paths.insert(0, self.file_path)
                with open(DIRECTORY_FILE, "w") as f:
                    f.writelines(p + "\n" for p in paths)
            # elif count == 7 or (count > 7 and paths[8] == ""):
            #     with open(DIRECTORY_FILE, "w") as f:
            #         paths = paths[0:6]
            #         paths.append(self.file_path)
            #         f.writelines(p + "\n" for p in paths)
            # elif count < 7:
            #     with open(DIRECTORY_FILE, "a") as f:
            #         f.writelines([self.file_path + "\n"])
        except Exception as e:
            with open(DIRECTORY_FILE, "w+") as f:
                f.write(self.file_path + "\n")

    ########### Heading ###########
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
        # title_edit = QtWidgets.QLineEdit()
        # name_edit = QtWidgets.QLineEdit()
        # config = configparser.ConfigParser()
        # config.read(CONFIG_FILE)
        # name = config['DEFAULT']['name']
        # name_edit.setText(name)
        # if self.name.text() != name:
        #     name_edit.setText(self.name.text())
        # title_edit.setText(self.heading_title.text())
        layout.addRow(self.tr("&Title:"), self.heading_title)
        layout.addRow(self.tr("&Name:"), self.heading_name)
        time_checkbox = QtWidgets.QCheckBox("Add Date", self)
        time_checkbox.setChecked(self.add_date) # Checked on by default
        dropdown = QtWidgets.QComboBox(self)
        for classes in name_classes:
            dropdown.addItem(classes)
        dropdown.addItem("---")
        dropdown.setCurrentText(self.heading_course.text())
        layout.addWidget(time_checkbox)
        layout.addRow(dropdown)
        add_button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        add_button.accepted.connect(
            lambda: self.accept_header(dropdown.currentText(), time_checkbox, header_dialog))
        add_button.rejected.connect(header_dialog.close)
        add_button.setOrientation(Qt.Horizontal)
        layout.addWidget(add_button)
        header_dialog.setLayout(layout)
        header_dialog.update()
        header_dialog.show()
        self.update()

    def accept_header(self, course, time_checkbox, dialog):
        if len(self.heading_title.text()) == 0 and len(self.heading_name.text()) == 0 and course == "---" and (not time_checkbox.isChecked()):
            #prompt to add at least one field
            error = QtWidgets.QMessageBox()
            error.setText("Please fill out at least one entry.")
            error.exec_()
            return
        # Update class selected and date bool
        self.heading_course.setText(course)
        self.add_date = time_checkbox.isChecked()
        # Get current date
        today = date.today()
        date_str = today.strftime("%B %d, %Y")
        #hello there how are you doing 5.5*len
        height = 1
        max_len = 3
        composed_heading = ""
        if len(self.heading_title.text()) != 0:
            composed_heading = "Title: " + self.heading_title.text() + "\n"
            if len(self.heading_title.text()) > max_len:
                max_len = len(self.heading_title.text())
            height = height + 1
        if len(self.heading_name.text()) != 0:
            composed_heading = composed_heading + "Name: " + self.heading_name.text() + "\n"
            if len(self.heading_name.text()) > max_len:
                max_len = len(self.heading_name.text())
            height = height + 1
        composed_heading = composed_heading + "Class: " + course + "\n"
        if len(course) > max_len:
            max_len = len(course)
        if time_checkbox.isChecked():
            composed_heading = composed_heading + "Date: " + date_str
            if len(date_str) > max_len:
                max_len = len(date_str)
            height = height + 1
        composed_heading = composed_heading.rstrip("\n")
        self.header_text.document().setPlainText(composed_heading)
        self.header_text.setFont(self.heading_font)
        xlen = (max_len+4)*self.heading_font.pointSize()
        ylen = height*self.heading_font.pointSize()*2
        self.header_text.setGeometry(0, 0, xlen, ylen)  # Dynamic sizing
        self.header_widget.deleteLater()
        self.header_widget = FloatingWidget(self.header_text, self.canvas_window)
        self.header_widget.show()
        dialog.close()
        self.update()
        return

    def settings(self):
        arial_font = QtGui.QFont("Times New Roman", 20, QtGui.QFont.Bold)
        font, ok = QtWidgets.QFontDialog.getFont(arial_font)
        if ok:
            self.heading_font = font
        dialog = QtWidgets.QDialog()
        time_checkbox = QtWidgets.QCheckBox("", self)
        time_checkbox.setChecked(self.add_date)
        self.accept_header( self.heading_course.text(), time_checkbox, dialog)

    def open(self, file_path:str=None):
        if self.canvas_window.label.hasChanged():
            self.savePopup()
        if not file_path:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/home", "JPG (*.jpg);;PNG (*.png)")
            if file_path == "":
                return
            self.file_path = file_path
        else:
            self.file_path = file_path
        self.open_directory(self.file_path)
        self.setWindowTitle(self.file_path)

    def update_open_recent_menu(self):
        try:
            with open(DIRECTORY_FILE, "r") as f:
                read_directories = f.readlines()
            f.close()
        except Exception as e:
            return False

        directories = []
        for i in read_directories:
            if os.path.isfile(i.strip()):
                directories.append(i)
        with open(DIRECTORY_FILE, "w") as f:
            f.writelines(p.strip() + "\n" for p in directories)

        if len(directories) == 0:
            return False
        else:
            #directories.reverse()
            self.open_recent_option.clear()
            dir_length = 7
            if len(directories) < 7:
                dir_length = len(directories)
            #for i in range(len(directories)):
            for i in range(dir_length):
                action = QAction(directories[i], self.open_recent_option)
                action.triggered.connect(lambda state, x=directories[i].strip(): self.open(x))
                self.open_recent_option.addAction(action)
            self.open_recent_option.setEnabled(True)
            return True

    def open_directory(self, file_path):
        if not os.path.isfile(file_path):
            if not self.scheduled:
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
            self.canvas_window.label.loadImage(file_path)

    def ocr(self):
        if self.canvas_window.label.hasChanged() or self.file_path == "":
            self.savePopup()
        if not self.canvas_window.label.hasChanged():
            ocr_findings = pytesseract.image_to_string(Image.open(self.file_path))
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