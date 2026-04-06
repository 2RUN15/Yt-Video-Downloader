from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction, QPixmap
import sys
import os
from FastWindow.fastdownact import FastApp
from MainWindow.mainwindowapp import MainWindow
from actions.functions_main import json_read, json_save
from SettingsWindow.settingsapp import SettingsWidget

APP_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(APP_PATH)
APP_ICON = f"{BASE_DIR}/../icons/app.png"

class ServiceWindow:
    def __init__(self):
        super().__init__()
        
        #NoneValus
        self.settingswin = None

        #TrayMenu
        self.tray = QSystemTrayIcon()
        self.icon = QIcon(APP_ICON)
        self.tray.setIcon(self.icon)
        self.menu = QMenu()
        
        #Action Ekleme
        self.action_actv = QAction("Activate")
        self.action_exit = QAction("Exit")
        self.action_settings = QAction("Settings")
        
        #Action Bağlantıları
        self.action_actv.triggered.connect(self.fast_proc_stat)
        self.action_actv.setCheckable(True)
        self.action_actv.setChecked(True)
        
        self.action_settings.triggered.connect(self.open_settings)
        
        self.action_exit.triggered.connect(QApplication.instance().quit)
        
        #Action'u menüye ekleme
        self.menu.addAction(self.action_actv)
        self.menu.addAction(self.action_settings)
        self.menu.addSeparator()
        self.menu.addAction(self.action_exit)
        
        #Çalıştırma
        self.tray.setContextMenu(self.menu)
        self.tray.show()

        #Windows
        self.fast_app = FastApp()        
        self.fast_app.link_found.connect(self.link_found)
        self.fast_app.start()
        
        self.main_ui = MainWindow()
        self.confpath = os.path.join(BASE_DIR,os.pardir,"config.json")
        
        #Remember Choice
        self.savedata = json_read(self.confpath)
        
        if self.savedata["remembermainchoice"] == False:
            self.savedata["remembermainchoice"] = False
            json_save(self.confpath, self.savedata)
            return self.main_ui.show()
    
    def fast_proc_stat(self, bool):
        if bool:
            self.fast_app.start()
        else:
            self.fast_app.stop()
    
    def link_found(self, link):
        print(link,flush=True)
    
    def open_settings(self):
        if hasattr(self, "settingswin") and self.settingswin is not None:
            self.settingswin.activateWindow()
            self.settingswin.raise_()
            return
        
        self.settingswin = SettingsWidget()
        
        self.settingswin.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.settingswin.destroyed.connect(self._on_settings_closed)
        
        self.settingswin.show()
    
    def _on_settings_closed(self):
        self.settingswin = None
        