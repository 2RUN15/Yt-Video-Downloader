from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from MainWindow.frontend import Ui_MainWindow
import sys
from PyQt6.QtGui import QGuiApplication
from actions.messagebox import FastInfo
from SettingsWindow.settingsapp import SettingsWidget
from actions.functions_main import json_save,json_read
import os

MAIN_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(MAIN_PATH)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(300,220)
        
        #PATHS
        self.configjsonpath = f"{BASE_DIR}/../config.json"
        self.saveddata = json_read(self.configjsonpath)
        
        #Style
        try:
            with open(f"{BASE_DIR}/style.qss", "r", encoding="utf-8") as f:
                style = f.read()
            self.setStyleSheet(style)
        except FileNotFoundError:
            print("Uyarı: style.qss dosyası bulunamadı!")
        
        #Dialogs
        self.fastinfo = FastInfo()
        
        #Windows
        self.settingsButtonWin = SettingsWidget()
        
        #Buttons
        self.ui.fastButton.clicked.connect(self.fastButton)
        
        self.ui.checkBox.toggled.connect(self.checkBox)
        
        self.ui.settingsButton.setIcon(QIcon(f"{BASE_DIR}/../icons/settings.png"))
        self.ui.settingsButton.setIconSize(QSize(32,32))
        self.ui.settingsButton.clicked.connect(self.settingsButtonFunc)
        
    def fastButton(self):
        self.saveddata = json_read(self.configjsonpath)
        self.saveddata["downmode"] = "fast"
        json_save(self.configjsonpath, self.saveddata)
        self.close()
        self.fastinfo.exec()
    
    def settingsButtonFunc(self):
        self.settingsButtonWin.show()
    
    def checkBox(self, ischeck):
        self.saveddata = json_read(self.configjsonpath)
        if ischeck:
            self.saveddata["remembermainchoice"] = True
        else:
            self.saveddata["remembermainchoice"] = False
        
        json_save(self.configjsonpath, self.saveddata)
        