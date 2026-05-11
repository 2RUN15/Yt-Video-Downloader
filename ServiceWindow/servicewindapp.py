from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction, QPixmap
import sys
import os
from actions.fastapp import FastApp
from actions.advancedapp import AdvancedApp
from MainWindow.mainwindowapp import MainWindow
from actions.functions_main import json_read, json_save
from SettingsWindow.settingsapp import SettingsWidget
from AdvancedWindow.advancedwindowapp import AdvancedWindow
import platform

APP_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(APP_PATH)
APP_ICON = f"{BASE_DIR}/../icons/app.png"

#Python ikonunu kaldırır
def set_mac_dock_icon_visible(visible):
    if platform.system() == "Darwin":
        try:
            from AppKit import NSApp, NSApplicationActivationPolicyRegular, NSApplicationActivationPolicyAccessory
            
            if visible:
                NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
            
            else:
                NSApp.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        except ImportError:
            pass

class ServiceWindow:
    def __init__(self):
        super().__init__()
        
        #DockVisible
        set_mac_dock_icon_visible(False)
        
        #NoneValus
        self.settingswin = None
        self.savedata = None
        self.downmode = None
        
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
        
        #Remember Choice
        self.confpath = os.path.join(BASE_DIR,os.pardir,"config.json")
        self.savedata = json_read(self.confpath)
        
        if self.savedata["remembermainchoice"] == False:
            self.main_ui = MainWindow()
            self.savedata["remembermainchoice"] = False
            json_save(self.confpath, self.savedata)
            self.main_ui.show()
        
        #Windows
        self.savedata = json_read(self.confpath)
        self.downmode = self.savedata["downmode"]
        if self.downmode == "fast":
            self.worker = FastApp()
            self.worker.start()
        elif self.downmode == "advanced":
            self.worker = AdvancedApp()
            self.worker.start()
    
    def fast_proc_stat(self, boolval):
        if boolval and self.downmode == "fast":
            self.worker.start()
        elif not boolval and self.downmode == "fast":
            self.worker.stop()
        
        if boolval and self.downmode == "advanced":
            self.worker.start()
        elif not boolval and self.downmode == "advanced":
            self.worker.stop()
    
    def open_settings(self):
        set_mac_dock_icon_visible(True)
        
        if hasattr(self, "worker") and self.worker:
            self.worker.stop()
        if hasattr(self, "settingswin") and self.settingswin is not None:
            self.settingswin.activateWindow()
            self.settingswin.raise_()
            return
        
        self.settingswin = MainWindow()
        
        self.settingswin.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.settingswin.destroyed.connect(self._on_settings_closed)
        
        self.settingswin.show()
    
    def start_worker(self):
        self.savedata = json_read(self.confpath)
        self.downmode = self.savedata["downmode"]
        
        if hasattr(self, "worker") and self.worker:
            self.worker.stop()

        if self.downmode == "fast":
            self.worker = FastApp()
        elif self.downmode == "advanced":
            self.worker = AdvancedApp()
            
        self.worker.update_settings()
        self.worker.start()
    
    def _on_settings_closed(self):
        self.settingswin = None
        set_mac_dock_icon_visible(False)
        if hasattr(self, "worker") and self.worker:
            self.worker.update_settings()
            self.start_worker()
        
        