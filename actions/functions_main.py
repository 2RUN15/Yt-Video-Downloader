import json
import os
import sys

def json_save(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=True)
    except Exception as e:
        raise e

def json_read(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise e

def file_read(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file = f.read()
        return file
    except Exception as e:
        raise e

def get_base_dir():
    try:
        base_path = sys._MEIPASS
    except Exception:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(current_dir)
    
    return base_path

def path_join(*file_paths):
    try:
        base_dir = get_base_dir()
        full_path = os.path.join(base_dir, *file_paths)
        return full_path
    except Exception as e:
        raise e

def get_conf_path():
    try:
        file_path = path_join("config.json")
        return file_path
    except Exception as e:
        raise e

def check_json(boolValue: bool):
    default_settings = {
        "video_format": "",
        "remembermainchoice": False,
        "downmode": "fast",
        "video_quality": "",
        "downlocation": "",
        "firstopen": True
    }
    
    conf_path = get_conf_path()
    if not os.path.isfile(conf_path) or boolValue:
        json_save(conf_path, default_settings)

def get_down_mode(index):
    if index == 0:
        return "fast"
    elif index == 1:
        return "advanced"
    elif index == 2:
        return "file"

def get_down_index(down_mode):
    if down_mode == "fast":
        return 0
    elif down_mode == "advanced":
        return 1
    elif down_mode == "file":
        return 2