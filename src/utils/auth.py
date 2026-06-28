import hashlib
import json
import os
import shutil

CREDENTIALS_FILE = "data/user_credentials.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    with open(CREDENTIALS_FILE, 'r') as f:
        credentials = json.load(f)
    if username in credentials:
        return credentials[username] == hash_password(password)
    return False

def create_user_account(username, password):
    with open(CREDENTIALS_FILE, 'r') as f:
        credentials = json.load(f)
    #username already exists
    if username in credentials:
        return False
    #add user credentials and initialize its directory
    credentials[username] = hash_password(password)
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f)
    initialize_user_folders(username)
    return True

def initialize_user_folders(username):
    user_folder = f"data/users/{username}"
    default_folder = f"data/default"
    if not os.path.exists(user_folder):
        os.mkdir(user_folder)
        if os.path.isfile(f"{default_folder}/muscles.json"):
            shutil.copy(f"{default_folder}/muscles.json", f"{user_folder}/muscles.json")
        if os.path.isfile(f"{default_folder}/exercises.json"):
            shutil.copy(f"{default_folder}/exercises.json", f"{user_folder}/exercises.json")