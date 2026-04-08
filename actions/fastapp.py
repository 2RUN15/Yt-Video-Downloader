from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from actions.copylisten import CopyListen
from actions.process import DownloadWideo
from packagevalues import vidoe_settings
from actions.functions_main import json_read, get_base_dir
import os
from NotificationWindow.notifapp import NotificationWindow

class FastApp:
    def __init__(self):
        super().__init__()
        
        #NoneValues
        self.video_format = None
        self.video_quality = None
        self.downlocation = None
        self.file_name = ""
        
        self.base_dir = get_base_dir()
        self.configjson_path = os.path.join(self.base_dir, os.pardir, "config.json")
        
        self.notification_window = NotificationWindow()
        
        self.copy_listen = CopyListen()
        self.copy_listen.link_found.connect(self.get_link)
        self.copy_listen.start()
        
        self.worker = None
    
    def start(self):
        self.copy_listen.start()
    
    def stop(self):
        self.copy_listen.stop()
    
    def get_link(self, link):

        if "youtube.com" not in link:
            return
        
        self.get_conf_json()

        result = self.notification_window.exec()
        
        if result == QFileDialog.DialogCode.Rejected:
            return
        
        self.video_values = vidoe_settings(
            video_format=self.video_format,
            video_quality=self.video_quality,
            file_path=self.downlocation,
            video_url=link,
            file_name = self.file_name
        )

        self.worker = DownloadWideo(self.video_values)
        self.worker.start()
        
    def get_conf_json(self):
        self.configjson = json_read(self.configjson_path)
        self.video_format = self.configjson["video_format"]
        self.video_quality = self.configjson["video_quality"][:-1]
        self.downlocation = self.configjson["downlocation"]
    