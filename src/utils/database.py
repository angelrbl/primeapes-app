import json
from src.utils.files import check_file
from src.models.Muscle import Muscle

def get_muscle_list(user):
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    muscle_list = []
    with open(MUSCLES_FILE, "r") as f:
        muscles_data = json.load(f)
    for muscle in muscles_data:
        muscle_list.append(Muscle.from_json(muscle))
    return muscle_list