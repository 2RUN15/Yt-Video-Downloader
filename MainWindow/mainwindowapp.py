from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from MainWindow.main_window_ui import Ui_MainWindow
import sys
from PyQt6.QtGui import QGuiApplication
from actions.messagebox import FastInfo
from SettingsWindow.settingsapp import SettingsWidget
from actions.functions_main import json_save,json_read,get_conf_path,file_read, path_join, get_down_index, get_down_mode
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(500,400)
        
        #PATHS
        self.configjsonpath = get_conf_path()
        self.saveddata = json_read(self.configjsonpath)
        self.iconPath = path_join("icons","settings.png")
        
        #Style
        style_path = path_join("assets","main_win.qss")
        style_File = file_read(style_path)
        self.setStyleSheet(style_File)
        
        #Default Settings
        self.down_mode = self.saveddata["downmode"]
        self.rem_my_choice = self.saveddata["remembermainchoice"]
        
        #First Open
        if self.down_mode:
            self.ui.down_modeComboB.setCurrentIndex(get_down_index(self.down_mode))
        
        self.ui.rem_my_choicCheckB.setChecked(self.rem_my_choice)
        
        #Dialogs
        self.fastinfo = FastInfo()
        
        #Windows
        self.settingsButtonWin = SettingsWidget()
        
        #Buttons
        self.ui.rem_my_choicCheckB.toggled.connect(self.checkBox)
        
        self.ui.down_modeComboB.currentIndexChanged.connect(self.get_down_mode_func)
        
        self.ui.settingsButton.setIcon(QIcon(self.iconPath))
        self.ui.settingsButton.setIconSize(QSize(32,32))
        self.ui.settingsButton.clicked.connect(self.settingsButtonFunc)
    
    def settingsButtonFunc(self):
        self.settingsButtonWin.show()
    
    def checkBox(self, ischeck):
        self.saveddata = json_read(self.configjsonpath)
        if ischeck:
            self.saveddata["remembermainchoice"] = True
        else:
            self.saveddata["remembermainchoice"] = False
        
        json_save(self.configjsonpath, self.saveddata)
    
    def get_down_mode_func(self, index):
        
        self.saveddata["downmode"] = get_down_mode(index)
        
        json_save(self.configjsonpath, self.saveddata)