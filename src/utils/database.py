import json
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise

def get_muscle_list(user):
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    muscle_list = []
    with open(MUSCLES_FILE, "r") as f:
        muscles_data = json.load(f)
    for muscle in muscles_data:
        muscle_list.append(Muscle.from_json(muscle))
    return muscle_list

def get_exercise_list(user):
    EXERCISE_FILE = check_file(f"{user.get_folder()}/exercises.json")
    user_muscles = get_muscle_list(user)
    muscle_map = {m.get_name(): m for m in user_muscles}
    exercise_list = []
    with open(EXERCISE_FILE, "r") as f:
        exercises_data = json.load(f)
    for exercise in exercises_data:
        exercise_list.append(Exercise.from_json(exercise, muscle_map))
    return exercise_list