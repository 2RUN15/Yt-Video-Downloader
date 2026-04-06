from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from SettingsWindow.settingui import Ui_Form
from actions.functions_main import json_save, json_read
from actions.dialogs import chose_folder
import os 

RUN_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(RUN_PATH)

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(460,280)
        
        self.configjsonpath = f"{BASE_DIR}/../config.json"
        
        #Buttons
        self.ui.okButton.clicked.connect(self.okButton)
        
        self.saveddata = json_read(self.configjsonpath)
        if self.saveddata:
            self.ui.formatBox.setCurrentText(self.saveddata["video_format"])
            self.ui.qualityBox.setCurrentText(self.saveddata["video_quality"])
    
    def okButton(self):
        video_format = self.ui.formatBox.currentText()
        video_quality = self.ui.qualityBox.currentText()
        self.saveddata["video_format"] = video_format
        self.saveddata["video_quality"] = video_quality
        json_save(self.configjsonpath, self.saveddata)
        self.close()