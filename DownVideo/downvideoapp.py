from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from DownVideo.downvideoui import Ui_Form

class DownVideo(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
