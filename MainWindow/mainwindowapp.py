from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from MainWindow.frontend import Ui_MainWindow
import sys
from PyQt6.QtGui import QGuiApplication
from actions.messagebox import FastInfo
from SettingsWindow.settingsapp import SettingsWidget
from actions.functions_main import json_save,json_read,get_conf_path,file_read, path_join
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(300,220)
        
        #PATHS
        self.configjsonpath = get_conf_path()
        self.saveddata = json_read(self.configjsonpath)
        self.iconPath = path_join("icons","settings.png")
        
        #Style
        style_path = path_join("MainWindow","style.qss")
        style_File = file_read(style_path)
        self.setStyleSheet(style_File)
        
        #Dialogs
        self.fastinfo = FastInfo()
        
        #Windows
        self.settingsButtonWin = SettingsWidget()
        
        #Buttons
        self.ui.fastButton.clicked.connect(self.fastButton)
        self.ui.advancedButton.clicked.connect(self.advancedButtonClicked)
        
        self.ui.checkBox.toggled.connect(self.checkBox)
        
        self.ui.settingsButton.setIcon(QIcon(self.iconPath))
        self.ui.settingsButton.setIconSize(QSize(32,32))
        self.ui.settingsButton.clicked.connect(self.settingsButtonFunc)
        
    def fastButton(self):
        self.saveddata = json_read(self.configjsonpath)
        self.saveddata["downmode"] = "fast"
        json_save(self.configjsonpath, self.saveddata)
        self.close()
        self.fastinfo.exec()
    
    def advancedButtonClicked(self):
        self.saveddata = json_read(self.configjsonpath)
        self.saveddata["downmode"] = "advanced"
        json_save(self.configjsonpath, self.saveddata)
        self.close()
    
    def settingsButtonFunc(self):
        self.settingsButtonWin.show()
    
    def checkBox(self, ischeck):
        self.saveddata = json_read(self.configjsonpath)
        if ischeck:
            self.saveddata["remembermainchoice"] = True
        else:
            self.saveddata["remembermainchoice"] = False
        
        json_save(self.configjsonpath, self.saveddata)
        