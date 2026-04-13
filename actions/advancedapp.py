from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from actions.copylisten import CopyListen
from AdvancedWindow.advancedwindowapp import AdvancedWindow

class AdvancedApp:
    def __init__(self):
        super().__init__()
        
        #CopyListen
        self.copy_listen = CopyListen()
        self.copy_listen.link_found.connect(self.link_found)
        self.copy_listen.start()
        
        #AdvancedWindow
        self.advanced_window = None
            
    def link_found(self, link):
        if "youtube.com" not in link:
            return
        
        if not hasattr(self, "advanced_window") or self.advanced_window is None:
            self.advanced_window = AdvancedWindow()
            
        try:
            self.advanced_window.set_link(link)
            self.advanced_window.show()
            self.advanced_window.raise_()
            self.advanced_window.activateWindow()
        except RuntimeError:
            self.advanced_window = AdvancedWindow()
            self.advanced_window.set_link(link)
            self.advanced_window.show()
    
    def start(self):
        self.copy_listen.start()
    
    def stop(self):
        self.copy_listen.stop()
    
