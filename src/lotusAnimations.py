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
from time import sleep

class Animations:
    ########### Fading ###########
    def fade_out(self, widget, time=1000, start=1, end=0):
        self.fading_effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.fading_effect)

        self.fading_out_animation = QtCore.QPropertyAnimation(self.fading_effect, b"opacity")
        self.fading_out_animation.setDuration(time)
        self.fading_out_animation.setStartValue(start)
        self.fading_out_animation.setEndValue(end)
        return self.fading_out_animation
        #self.fading_out_animation.start()

    def fade_in(self, widget, time=1000, start=0, end=1):
        fading_effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(fading_effect)

        self.fading_in_animation = QtCore.QPropertyAnimation(fading_effect, b"opacity")
        self.fading_in_animation.setDuration(time)
        self.fading_in_animation.setStartValue(start)
        self.fading_in_animation.setEndValue(end)
        return self.fading_in_animation
        #self.fading_in_animation.start()