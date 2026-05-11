from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from ServiceWindow.servicewindapp import ServiceWindow
import sys
from PyQt6.QtGui import QGuiApplication
from actions.messagebox import FastInfo
import os


class StartWindow(ServiceWindow):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    service = StartWindow()
    sys.exit(app.exec())
