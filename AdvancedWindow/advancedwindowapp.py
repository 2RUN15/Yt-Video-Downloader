from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
from AdvancedWindow.advanced_window_ui import Ui_Form
from actions.functions_main import path_join, file_read, json_read, get_conf_path
from actions.dialogs import chose_folder
from actions.messagebox import WarningMess
from packagevalues import vidoe_settings, warningmesspack
from actions.process import DownloadWideo

class AdvancedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #JsonFile
        self.confPath = get_conf_path()
        self.confFile = json_read(self.confPath)
        
        #EmptyValues
        self.link = ""
        self.file_name = ""
        self.loc = ""
        self.worker = ""
        
        #DefaultValue
        self.defaultloc = self.confFile["downlocation"]

        
        style_path = path_join("assets","advanced_win.qss")
        self.style = file_read(style_path)
        self.setStyleSheet(self.style)

        #Buttons
        self.ui.audio_quality_slider.valueChanged.connect(self.change_line)
        
        self.ui.down_locationButton.clicked.connect(self.get_down_loc)
        
        self.ui.default_locCheckB.stateChanged.connect(self.get_check_index)
        
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
        
        if not self.loc:
            self.warning_packet = warningmesspack(
                window_title="WARNING!!!",
                text="Download Location not choosed. Please make sure you select your download location."
            )
            self.warning_win = WarningMess(self.warning_packet)
            self.warning_win.exec()
            
            return
        
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
    
    def get_down_loc(self):
        self.ui.default_locCheckB.setDisabled(True)
        down_loc = chose_folder(self)
        self.ui.down_locLine.setText(down_loc)
        
        self.loc =  down_loc
        self.ui.default_locCheckB.setEnabled(True)
    
    def get_check_index(self, index):
        if index == 2:
            self.ui.down_locationButton.setDisabled(True)
            self.ui.down_locLine.setText(self.defaultloc)
            self.loc = self.defaultloc
            
        elif index == 0:
            self.ui.down_locationButton.setEnabled(True)
            self.ui.down_locLine.clear()
            self.loc = ""
    
    def update_settings(self):
        self.confFile = json_read(self.confPath)