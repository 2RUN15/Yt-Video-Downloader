from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from SettingsWindow.settingui import Ui_Form
from actions.functions_main import json_save, json_read
from actions.dialogs import chose_folder
import os
from packagevalues import warningmesspack
from actions.messagebox import WarningMess

RUN_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(RUN_PATH)


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(460, 280)
        
        #None Values
        self.folder_path = None
        
        self.text = "Please choose download location"
        self.window_tittle = "WARNING!"

        self.configjsonpath = os.path.join(BASE_DIR, os.pardir, "config.json")

        # Buttons
        self.ui.okButton.clicked.connect(self.okButton)
        self.ui.chooselocButton.clicked.connect(self.choose_folder)

        self.saveddata = json_read(self.configjsonpath)
        if self.saveddata:
            self.ui.formatBox.setCurrentText(self.saveddata["video_format"])
            self.ui.qualityBox.setCurrentText(self.saveddata["video_quality"])
            self.ui.file_path_line.setText(self.saveddata["downlocation"])

        #QMessages
        self.downloccarr_pack = warningmesspack(window_title=self.window_tittle, text=self.text)
        self.downlocwarr = WarningMess(self.downloccarr_pack)

    def okButton(self):
        download_location = self.ui.file_path_line.text()
        if not download_location:
            return self.downlocwarr.exec()
        
        video_format = self.ui.formatBox.currentText()
        video_quality = self.ui.qualityBox.currentText()
        self.saveddata["video_format"] = video_format
        self.saveddata["video_quality"] = video_quality
        self.saveddata["downlocation"] = download_location
        json_save(self.configjsonpath, self.saveddata)
        self.close()

    def choose_folder(self):
        folder_path = chose_folder(self)
        self.ui.file_path_line.setText(folder_path)