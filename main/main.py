from PyQt6.QtWidgets import QApplication
from app import gui
import sys
import os

app = QApplication(sys.argv)
qss_path = os.path.join('main', 'style/style.qss')
if os.path.exists(qss_path):
    with open(qss_path, 'r') as f:
        app.setStyleSheet(f.read())
else:
    print("QSS file not found!")

window = gui()
window.show()
app.exec()
