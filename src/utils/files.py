import os
import shutil
import json
from src.utils.database import load_json_data, save_json_data

def initialize_user_folders(user):
    user_folder = user.get_folder()
    default_folder = f"data/default"
    
    if os.path.isfile(f"{default_folder}/muscles.json"):
        shutil.copy(f"{default_folder}/muscles.json", f"{user_folder}/muscles.json")
    if os.path.isfile(f"{default_folder}/exercises.json"):
        shutil.copy(f"{default_folder}/exercises.json", f"{user_folder}/exercises.json")

def check_file(FILE_PATH):
    if not os.path.isfile(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)
    return FILE_PATH

def delete_folder(FILE_PATH):
    if os.path.exists(FILE_PATH):
        shutil.rmtree(FILE_PATH)
        return True
    return False  