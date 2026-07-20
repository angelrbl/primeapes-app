import hashlib
from src.models.User import User
from src.utils.database import load_json_data, save_json_data, delete_folder, check_file, initialize_user_folders

CREDENTIALS_FILE = check_file("data/user_credentials.json", file_type=dict)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    credentials = load_json_data(CREDENTIALS_FILE)
    if username in credentials:
        return credentials[username] == hash_password(password)
    return False

def create_user_account(username, password):
    credentials = load_json_data(CREDENTIALS_FILE, default_type=dict)
    #username already exists
    if username in credentials:
        return False
    #add user credentials and initialize its directory
    credentials[username] = hash_password(password)
    if save_json_data(CREDENTIALS_FILE, credentials):
        return True
    return False

def initialize_new_user(user_id, name, weight, height):
    USER_FILE = check_file("data/users.json")
    users_data = load_json_data(USER_FILE)
    user = User(id=user_id, name=name, weight=weight, height=height)
    users_data.append(user.to_json())
    save_json_data(USER_FILE, users_data)
    print(users_data)
    initialize_user_folders(user, bodyweight=weight)
    return user

def initialize_user(user_id):
    USER_FILE = check_file("data/users.json")
    users_data = load_json_data(USER_FILE)
    for user in users_data:
        if user["id"] == user_id:
            user = User.from_json(user)
            return user
    return None

def delete_user(user):
    USER_FILE = check_file("data/users.json")
    CREDENTIALS_FILE = check_file("data/user_credentials.json")
    USER_FOLDER = f"data/users/{user.get_id()}"
    users_data = load_json_data(USER_FILE)
    credentials = load_json_data(CREDENTIALS_FILE)
    del credentials[user.get_id()]
    save_json_data(CREDENTIALS_FILE, credentials)
    for user_data in users_data:
        if user_data["id"] == user.get_id():
            users_data.remove(user_data)
            if save_json_data(USER_FILE, users_data):
                delete_folder(USER_FOLDER)
                return True
    return False