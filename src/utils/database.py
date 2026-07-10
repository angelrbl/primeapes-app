import json
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.models.Microcycle import Microcycle

def get_muscle_list(user):
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    muscle_list = []
    with open(MUSCLES_FILE, "r") as f:
        muscles_data = json.load(f)
    for muscle in muscles_data:
        muscle_list.append(Muscle.from_json(muscle))
    return muscle_list

def get_exercise_list(user):
    EXERCISES_FILE = check_file(f"{user.get_folder()}/exercises.json")
    user_muscles = get_muscle_list(user)
    muscle_map = {m.get_name(): m for m in user_muscles}
    exercise_list = []
    with open(EXERCISES_FILE, "r") as f:
        exercises_data = json.load(f)
    for exercise in exercises_data:
        exercise_list.append(Exercise.from_json(exercise, muscle_map))
    return exercise_list

def get_workout_list(user):
    WORKOUTS_FILE = check_file(f"{user.get_folder()}/workouts.json")
    user_exercises = get_exercise_list(user)
    exercise_map = {ex.get_name(): ex for ex in user_exercises}
    workout_list = []
    with open(WORKOUTS_FILE, "r") as f:
        workouts_data = json.load(f)
    for workout in workouts_data:
        workout_list.append(Workout.from_json(workout, exercise_map))
    return workout_list

def get_microcycle_list(user):
    MICROCYCLES_LIST = check_file(f"{user.get_folder()}/microcycles.json")
    user_workouts = get_workout_list(user)
    workout_map = {wrk.get_name(): wrk for wrk in user_workouts}
    microcycle_list = []
    with open(MICROCYCLES_LIST, "r") as f:
        microcycles_data = json.load(f)
    for microcycle in microcycles_data:
        microcycle_list.append(Microcycle.from_json(microcycle, workout_map))
    return microcycle_list

def get_categories_list(user):
    user_muscles = get_muscle_list(user=user)
    categories = set()
    for muscle in user_muscles:
        for category in muscle.get_categories():
            formatted_category = category.replace("_", " ").title()
            categories.add(formatted_category)
    return sorted(list(categories))

def get_categories_dict(user):
    user_muscles = get_muscle_list(user=user)
    categories_dict = {}
    for muscle in user_muscles:
        for category in muscle.get_categories():
            formatted_category = category.replace("_", " ").title()
            formatted_muscle = muscle.get_name().replace("_", " ").title()
            if formatted_category not in categories_dict.keys():
                categories_dict[formatted_category] = [formatted_muscle]
            else:
                categories_dict[formatted_category].append(formatted_muscle)
    return categories_dict

def load_json_data(file_path):
    with open(file_path, 'r') as f:
            file_data = json.load(f)
    return file_data

def save_json_data(file_path, file_data):
    with open(file_path, 'w') as f:
        json.dump(file_data, f, default=str)
        return True
    return False