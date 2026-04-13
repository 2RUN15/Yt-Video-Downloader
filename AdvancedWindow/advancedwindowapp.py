from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
from AdvancedWindow.advanced_window_ui import Ui_Form
from actions.functions_main import path_join, file_read, json_read
from packagevalues import vidoe_settings
from actions.process import DownloadWideo

class AdvancedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #EmptyValues
        self.link = ""
        self.file_name = ""
        self.loc = "/Users/tuakpina/Desktop"
        self.worker = ""
        
        style_path = path_join(["AdvancedWindow","style.qss"])
        self.style = file_read(style_path)
        self.setStyleSheet(self.style)

        #Buttons
        self.ui.audio_quality_slider.valueChanged.connect(self.change_line)
        
        self.ui.startButtonV.clicked.connect(self.start)
        self.ui.cancelButtonV.clicked.connect(self.cancel)
        
        self.ui.startButtonA.clicked.connect(self.start)
        self.ui.cancelButtonA.clicked.connect(self.cancel)
    
    def start(self):
        currenttab = self.ui.tabWidget.currentIndex()
        if currenttab == 0:
            return self.down_video_func()
        else:
            return self.down_audio_func()
    
    def cancel(self):
        self.close()

    def change_line(self, value):
        self.ui.audio_quality_line.setText(f"{value}kbs")
    
    def down_video_func(self):
        video_format = self.ui.video_format_box.currentText().lower()
        video_quality = self.ui.video_quality_box.currentText()[:-1]
        
        values = vidoe_settings(
            video_format=video_format,
            video_quality=video_quality,
            file_path=self.loc,
            video_url=self.link,
            file_name=self.file_name
        )
        
        self.worker = DownloadWideo(values)
        self.worker.start()
        self.close()

    def down_audio_func(self):
        pass
    
    def set_link(self, link):
        self.link = link
            