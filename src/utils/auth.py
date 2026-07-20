import hashlib
from src.models.User import User
from src.utils.database import get_data_fast, save_data_fast, delete_folder, check_file, initialize_user_folders

CREDENTIALS_FILE = check_file("data/user_credentials.json", file_type=dict)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    credentials = get_data_fast(CREDENTIALS_FILE)
    if username in credentials:
        return credentials[username] == hash_password(password)
    return False

def create_user_account(username, password):
    credentials = get_data_fast(CREDENTIALS_FILE)
    #username already exists
    if username in credentials:
        return False
    #add user credentials and initialize its directory
    credentials[username] = hash_password(password)
    if save_data_fast(CREDENTIALS_FILE, credentials):
        return True
    return False

def initialize_new_user(user_id, name, weight, height):
    USER_FILE = check_file("data/users.json")
    users_data = get_data_fast(USER_FILE)
    user = User(id=user_id, name=name, weight=weight, height=height)
    users_data.append(user.to_json())
    save_data_fast(USER_FILE, users_data)
    initialize_user_folders(user, bodyweight=weight)
    return user

def initialize_user(user_id):
    USER_FILE = check_file("data/users.json")
    users_data = get_data_fast(USER_FILE)
    for user in users_data:
        if user["id"] == user_id:
            user = User.from_json(user)
            return user
    return None

def delete_user(user):
    USER_FILE = check_file("data/users.json")
    CREDENTIALS_FILE = check_file("data/user_credentials.json", file_type=dict)
    USER_FOLDER = f"data/users/{user.get_id()}"
    users_data = get_data_fast(USER_FILE)
    credentials = get_data_fast(CREDENTIALS_FILE)
    del credentials[user.get_id()]
    save_data_fast(CREDENTIALS_FILE, credentials)
    for user_data in users_data:
        if user_data["id"] == user.get_id():
            users_data.remove(user_data)
            if save_data_fast(USER_FILE, users_data):
                delete_folder(USER_FOLDER)
                return True
    return False