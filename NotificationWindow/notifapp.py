from NotificationWindow.frontend import Ui_Form
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QGuiApplication

# 1. QWidget yerine QDialog miras alıyoruz
class NotificationWindow(QDialog):
    # Sinyale artık ihtiyacın kalmayabilir çünkü exec() doğrudan değer döndürür, 
    # ama yapıya dokunmuyorum, istersen kalabilir.
    result_signal = pyqtSignal(bool) 
    
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Pencereyi özelleştiriyoruz
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.ToolTip)
        
        self.locate_screen()
        
        # 2. Buton bağlantılarını QDialog'un yerleşik metotlarına bağlıyoruz
        self.ui.yesButton.clicked.connect(self.accept) # accept() -> exec'den 1 döner
        self.ui.noButton.clicked.connect(self.reject)  # reject() -> exec'den 0 döner
        
    def locate_screen(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        # Pencere boyutunu tam alabilmek için layout'u güncelliyoruz
        self.adjustSize() 
        screen_size = self.frameGeometry()
        
        x = screen.width() - screen_size.width() - 20
        y = screen.height() - screen_size.height() - 20
        
        self.move(x, y)
    
    # QDialog kullanırken yes_button ve no_button metotlarını 
    # doğrudan accept/reject bağladığımız için bunlara teknik olarak gerek kalmadı.
    # Ancak özel bir işleme yapacaksan yine de kullanabilirsin:
    def yes_button(self):
        self.accept()
    
    def no_button(self):
        self.reject()
        
    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter:
            self.accept()
        elif a0.key() == Qt.Key.Key_Escape:
            self.reject()