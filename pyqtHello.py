import wsl
from PyQt5.QtWidgets import *

wsl.set_display_to_host()

app = QApplication([])
label = QLabel('Hello World!')
label.show()
app.exec_()