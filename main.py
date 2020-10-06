import wsl

wsl.set_display_to_host()

from PyQt5.QtWidgets import *
app = QApplication([])
label = QLabel('Hello World!')
label.show()
app.exec_()