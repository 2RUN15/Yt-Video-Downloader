from PyQt6.QtWidgets import QMessageBox
from packagevalues import warningmesspack

class FileChosErr(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WARNING!")
        self.setText("The File is not choosed")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)

class FolderPathErr(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WARNING!")
        self.setText("The folder path is not choosed")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)
        
class ReturnErr(QMessageBox):
    def __init__(self,error):
        self.error = error
        super().__init__()
        self.setWindowTitle("ERROR!")
        self.setText(f"{self.error}")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Critical)
        
class FastInfo(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("INFO")
        self.setText("Fast Download listens to the websites you've copied in the background.\n\nIt allows you to download easily with the default settings.")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Information)

class WarningMess(QMessageBox):
    def __init__(self, conf: warningmesspack):
        super().__init__()
        self.setWindowTitle(f"{conf.window_title}")
        self.setText(f"{conf.text}")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)