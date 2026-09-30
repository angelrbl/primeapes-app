import json
import os
import shutil
from datetime import datetime as dt

from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.models.Microcycle import Microcycle
from src.models.Macrocycle import Macrocycle


# ---------------------------------------------------------------------------
# Carpetas y ficheros
# ---------------------------------------------------------------------------
def check_folder(FOLDER_PATH):
    os.makedirs(FOLDER_PATH, exist_ok=True)
    return FOLDER_PATH


def check_file(FILE_PATH, file_type=list):
    """Crea el fichero JSON vacío ([] o {}) si no existe y devuelve su ruta."""
    CLEAN_PATH = FILE_PATH.strip("/")

    if not os.path.isfile(CLEAN_PATH):
        save_json_data(CLEAN_PATH, {} if file_type == dict else [])

    return CLEAN_PATH


def delete_folder(FILE_PATH):
    if os.path.exists(FILE_PATH):
        shutil.rmtree(FILE_PATH)
        return True
    return False


def initialize_user_folders(user, bodyweight=None):
    user_folder = check_folder(user.get_folder())
    default_folder = "data/default"

    for filename in ("muscles.json", "exercises.json"):
        default_file = f"{default_folder}/{filename}"
        if os.path.isfile(default_file):
            shutil.copy(default_file, f"{user_folder}/{filename}")

    if bodyweight:
        save_json_data(
            f"{user_folder}/bodyweight_history.json",
            [{"date": dt.today().date().strftime('%Y-%m-%d'), "weight": bodyweight}],
        )


# ---------------------------------------------------------------------------
# Lectura / escritura JSON
# ---------------------------------------------------------------------------
def load_json_data(file_path):
    """Devuelve el contenido del JSON, o None si no existe o está corrupto."""
    clean_path = file_path.strip("/")

    if not os.path.isfile(clean_path):
        return None

    try:
        with open(clean_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error while reading '{clean_path}': {e}")
        return None


def save_json_data(file_path, file_data):
    clean_path = file_path.strip("/")

    try:
        folder = os.path.dirname(clean_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Se escribe primero en un temporal para no corromper el fichero si algo falla
        tmp_path = f"{clean_path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=4, ensure_ascii=False, default=str)
        os.replace(tmp_path, clean_path)
        return True
    except OSError as e:
        print(f"Error while saving '{clean_path}': {e}")
        return False


# Alias para no romper el resto de la app (antes tenían caché en session_state)
def get_data_fast(file_path: str):
    return load_json_data(file_path)


def save_data_fast(file_path: str, data) -> bool:
    return save_json_data(file_path, data)


# ---------------------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------------------
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


def get_macrocycle_list(user):
    MACROCYCLES_FILE = check_file(f"{user.get_folder()}/macrocycles.json")
    user_microcycles = get_microcycle_list(user)
    microcycle_map = {mic.get_id(): mic for mic in user_microcycles}
    macrocycle_list = []
    macrocycles_data = load_json_data(MACROCYCLES_FILE)
    for macrocycle in macrocycles_data:
        macrocycle_list.append(Macrocycle.from_json(macrocycle, microcycle_map))
    return macrocycle_list


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


# ---------------------------------------------------------------------------
# Peso corporal y medidas
# ---------------------------------------------------------------------------
def get_bodyweight_history_list(user):
    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    return load_json_data(BODYWEIGHT_HISTORY_FILE)


def get_measurements_history_list(user):
    MEASUREMENTS_HISTORY_FILE = check_file(f"{user.get_folder()}/measurements_history.json")
    return load_json_data(MEASUREMENTS_HISTORY_FILE)


def add_weigh_in(user, weight, date=None):
    if date is None:
        date = dt.today().date()

    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    USERS_FILE = check_file("data/users.json")

    user_bodyweight_history = get_bodyweight_history_list(user)
    date_str = date.strftime('%Y-%m-%d')

    date_exists = False
    for entry in user_bodyweight_history:
        if entry["date"] == date_str:
            entry["weight"] = weight
            date_exists = True
            break

    if not date_exists:
        user_bodyweight_history.append({"date": date_str, "weight": weight})

    user_bodyweight_history = sorted(
        user_bodyweight_history,
        key=lambda x: dt.strptime(x["date"], '%Y-%m-%d').date(),
    )
    save_json_data(BODYWEIGHT_HISTORY_FILE, user_bodyweight_history)

    if user_bodyweight_history[-1]["date"] == date_str:
        user.set_weight(weight)

        users_data = load_json_data(USERS_FILE)
        for user_data in users_data:
            if user_data["id"] == user.get_id():
                user_data["weight"] = weight
                break
        save_json_data(USERS_FILE, users_data)
    return True