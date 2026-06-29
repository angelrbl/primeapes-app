import hashlib
import json
from src.utils.files import *
from src.models.User import User

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
    return True

def initialize_new_user(user_id, name, weight, height):
    USER_FILE = "data/users.json"
    with open(USER_FILE, "r") as f:
        users_data = json.load(f)
    user = User(user_id=user_id, name=name, weight=weight, height=height)
    print(user)
    users_data.append(user.to_json())
    with open(USER_FILE, "w") as f:
        json.dump(users_data, f)
    initialize_user_folders(user)
    return user

def initialize_user(user_id):
    USER_FILE = "data/users.json"
    with open(USER_FILE, "r") as f:
        users_data = json.load(f)
    for user in users_data:
        if user["user_id"] == user_id:
            user = User.from_json(user)
            return user
    return None