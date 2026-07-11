import json
from datetime import datetime as dt
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.models.Microcycle import Microcycle

def load_json_data(file_path):
    with open(file_path, 'r') as f:
            file_data = json.load(f)
    return file_data

def save_json_data(file_path, file_data):
    with open(file_path, 'w') as f:
        json.dump(file_data, f, default=str)
        return True
    return False

def get_muscle_list(user):
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    muscle_list = []
    muscles_data = load_json_data(MUSCLES_FILE)
    for muscle in muscles_data:
        muscle_list.append(Muscle.from_json(muscle))
    return muscle_list

def get_exercise_list(user):
    EXERCISES_FILE = check_file(f"{user.get_folder()}/exercises.json")
    user_muscles = get_muscle_list(user)
    muscle_map = {m.get_name(): m for m in user_muscles}
    exercise_list = []
    exercises_data = load_json_data(EXERCISES_FILE)
    for exercise in exercises_data:
        exercise_list.append(Exercise.from_json(exercise, muscle_map))
    return exercise_list

def get_workout_list(user):
    WORKOUTS_FILE = check_file(f"{user.get_folder()}/workouts.json")
    user_exercises = get_exercise_list(user)
    exercise_map = {ex.get_name(): ex for ex in user_exercises}
    workout_list = []
    workouts_data = load_json_data(WORKOUTS_FILE)
    for workout in workouts_data:
        workout_list.append(Workout.from_json(workout, exercise_map))
    return workout_list

def get_microcycle_list(user):
    MICROCYCLES_FILE = check_file(f"{user.get_folder()}/microcycles.json")
    user_workouts = get_workout_list(user)
    workout_map = {wrk.get_name(): wrk for wrk in user_workouts}
    microcycle_list = []
    microcycles_data = load_json_data(MICROCYCLES_FILE)
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

def get_bodyweight_history_list(user):
    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    bodyweight_history_data = load_json_data(BODYWEIGHT_HISTORY_FILE)
    bodyweight_history = []
    for bodyweight in bodyweight_history_data:
        bodyweight_history.append(bodyweight)
    return bodyweight_history


def add_weigh_in(user, weight, date = dt.today().date()):
    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    USERS_FILE = check_file(f"data/users.json")
    user_bodyweight_history = get_bodyweight_history_list(user)

    weigh_in = {
        "date": date.strftime('%Y-%m-%d'),
        "weight": weight
    }

    for i in range(len(user_bodyweight_history)):
        if dt.strptime(user_bodyweight_history[-i]["date"], '%Y-%m-%d').date() == date:
            user_bodyweight_history[-i]["weight"] = weight
            if i == 1:
                users_data = load_json_data(USERS_FILE)
                user.set_weight(weight)
                for user_data in users_data:
                    if user_data["user_id"] == user.get_id():
                        user_data = user.to_json()
                save_json_data(USERS_FILE, users_data)
            break
        elif dt.strptime(user_bodyweight_history[i]["date"], '%Y-%m-%d').date() == date:
            user_bodyweight_history[i]["weight"] = weight
            break
        elif dt.strptime(user_bodyweight_history[-i]["date"], '%Y-%m-%d').date() < date:
            user_bodyweight_history.insert(len(user_bodyweight_history)-i, weigh_in)
            if i == 1:
                users_data = load_json_data(USERS_FILE)
                user.set_weight(weight)
                print(user.get_weight())
                for user_data in users_data:
                    if user_data["user_id"] == user.get_id():
                        user_data = user.to_json()
                save_json_data(USERS_FILE, users_data)
            break
        elif dt.strptime(user_bodyweight_history[i]["date"], '%Y-%m-%d').date() > date:
            user_bodyweight_history.insert(i, weigh_in)
            break

    if save_json_data(BODYWEIGHT_HISTORY_FILE, user_bodyweight_history):
        return True
    return False
