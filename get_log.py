import os
import sys
import logging

def get_log_dir(app_name="Yt-Downloader") -> str:
    """İşletim sistemine göre güvenli log klasörünün yolunu döndürür."""
    
    if sys.platform == "win32":
        # Windows: AppData/Local
        base_dir = os.getenv('LOCALAPPDATA', os.path.expanduser('~'))
        return os.path.join(base_dir, app_name, "Logs")
        
    elif sys.platform == "darwin":
        # macOS: ~/Library/Logs
        base_dir = os.path.expanduser('~/Library/Logs')
        return os.path.join(base_dir, app_name)
        
    else:
        # Linux (veya diğer Unix sistemler): ~/.local/share
        # XDG Base Directory standartlarına uyum sağlıyoruz
        base_dir = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        return os.path.join(base_dir, app_name, "Logs")

def log_al(name: str, dosya_ismi: str = "app.log") -> logging.Logger:
    
    # 1. İşletim sistemine uygun klasörü bul
    log_klasoru = get_log_dir()
    
    # 2. Eğer o klasör ağacı henüz bilgisayarda yoksa, sessizce oluştur
    if not os.path.exists(log_klasoru):
        os.makedirs(log_klasoru)
        
    # 3. Log dosyamızın nihai ve evrensel güvenli yolu
    tam_yol = os.path.join(log_klasoru, dosya_ismi)

    # --- Loglama Ayarları ---
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.hasHandlers():
        dosya_handler = logging.FileHandler(tam_yol, encoding='utf-8')
        dosya_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        dosya_handler.setFormatter(formatter)
        
        logger.addHandler(dosya_handler)
        
    return logger