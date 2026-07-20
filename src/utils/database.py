from datetime import datetime as dt
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.models.Microcycle import Microcycle
from src.models.Macrocycle import Macrocycle
from supabase import Client, create_client
import streamlit as st
import json


@st.cache_resource
def init_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase_client()
if supabase:
    print("Supabase successfully initialized.")
BUCKET_NAME = "app-data"

def get_data_fast(file_path: str):
    key = f"cache_{file_path.strip('/')}"
    
    if key not in st.session_state:
        st.session_state[key] = load_json_data(file_path)
        
    return st.session_state[key]

def save_data_fast(file_path: str, data) -> bool:
    key = f"cache_{file_path.strip('/')}"
    st.session_state[key] = data

    return save_json_data(file_path, data)

def load_json_data(file_path: str):
    clean_path = file_path.strip("/")
    
    try:
        data_bytes = supabase.storage.from_(BUCKET_NAME).download(clean_path)
        return json.loads(data_bytes.decode("utf-8"))
    except Exception:
        return None

def save_json_data(file_path: str, file_data):
    clean_path = file_path.strip("/")
    json_bytes = json.dumps(file_data, indent=4, ensure_ascii=False).encode("utf-8")
    
    file_options = {
        "content-type": "application/json",
        "upsert": "true"
    }
    
    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            path=clean_path,
            file=json_bytes,
            file_options=file_options
        )
        return True
    except Exception:
        try:
            supabase.storage.from_(BUCKET_NAME).update(
                path=clean_path,
                file=json_bytes,
                file_options={"content-type": "application/json"}
            )
            return True
        except Exception as e:
            print(f"Error while saving '{clean_path}' on Supabase: {e}")
            return False

def delete_folder(FILE_PATH):
    try:
        files_in_folder = supabase.storage.from_(BUCKET_NAME).list(FILE_PATH)

        if files_in_folder:
            files_to_delete = [f"{FILE_PATH}/{f['name']}" for f in files_in_folder]
            supabase.storage.from_(BUCKET_NAME).remove(files_to_delete)

        return True
    except Exception as e:
        print(f"Error deleting folder {FILE_PATH} from Supabase: {e}")
        return False

def check_file(FILE_PATH, file_type = list):
    CLEAN_PATH = FILE_PATH.strip("/")

    if file_type == dict:
        data = get_data_fast(CLEAN_PATH)
        if not data:
            save_data_fast(CLEAN_PATH, {})
            return CLEAN_PATH
    else:
        data = get_data_fast(CLEAN_PATH)

        if not data:
            if save_data_fast(CLEAN_PATH, []):
                return CLEAN_PATH
        
    return CLEAN_PATH

def initialize_user_folders(user, bodyweight):
    user_folder = user.get_folder()
    default_folder = f"data/default"
    
    default_muscles = get_data_fast(f"{default_folder}/muscles.json")
    default_exercises = get_data_fast(f"{default_folder}/exercises.json")
    
    if default_muscles:
        save_data_fast(f"{user_folder}/muscles.json", default_muscles)
    if default_exercises:
        save_data_fast(f"{user_folder}/exercises.json", default_exercises)
    if bodyweight:
        save_data_fast(f"{user_folder}/bodyweight_history.json", [{"date": dt.today().date().strftime('%Y-%m-%d'), "weight": bodyweight}])

def get_muscle_list(user):
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    muscle_list = []
    muscles_data = get_data_fast(MUSCLES_FILE)
    for muscle in muscles_data:
        muscle_list.append(Muscle.from_json(muscle))
    return muscle_list

def get_exercise_list(user):
    EXERCISES_FILE = check_file(f"{user.get_folder()}/exercises.json")
    user_muscles = get_muscle_list(user)
    muscle_map = {m.get_name(): m for m in user_muscles}
    exercise_list = []
    exercises_data = get_data_fast(EXERCISES_FILE)
    for exercise in exercises_data:
        exercise_list.append(Exercise.from_json(exercise, muscle_map))
    return exercise_list

def get_workout_list(user):
    WORKOUTS_FILE = check_file(f"{user.get_folder()}/workouts.json")
    user_exercises = get_exercise_list(user)
    exercise_map = {ex.get_name(): ex for ex in user_exercises}
    workout_list = []
    workouts_data = get_data_fast(WORKOUTS_FILE)
    for workout in workouts_data:
        workout_list.append(Workout.from_json(workout, exercise_map))
    return workout_list

def get_microcycle_list(user):
    MICROCYCLES_FILE = check_file(f"{user.get_folder()}/microcycles.json")
    user_workouts = get_workout_list(user)
    workout_map = {wrk.get_name(): wrk for wrk in user_workouts}
    microcycle_list = []
    microcycles_data = get_data_fast(MICROCYCLES_FILE)
    for microcycle in microcycles_data:
        microcycle_list.append(Microcycle.from_json(microcycle, workout_map))
    return microcycle_list

def get_macrocycle_list(user):
    MACROCYCLES_FILE = check_file(f"{user.get_folder()}/macrocycles.json")
    user_microcycles = get_microcycle_list(user)
    microcycle_map = {mic.get_id(): mic for mic in user_microcycles}
    macrocycle_list = []
    macrocycles_data = get_data_fast(MACROCYCLES_FILE)
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

def get_bodyweight_history_list(user):
    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    return get_data_fast(BODYWEIGHT_HISTORY_FILE)

def get_measurements_history_list(user):
    MEASUREMENTS_HISTORY_FILE = check_file(f"{user.get_folder()}/measurements_history.json")
    return get_data_fast(MEASUREMENTS_HISTORY_FILE)

def add_weigh_in(user, weight, date = None):
    if date is None:
        date = dt.today().date()

    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    USERS_FILE = check_file(f"data/users.json")

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

    user_bodyweight_history = sorted(user_bodyweight_history, key=lambda x: dt.strptime(x["date"], '%Y-%m-%d').date())
    save_data_fast(BODYWEIGHT_HISTORY_FILE, user_bodyweight_history)

    if user_bodyweight_history[-1]["date"] == date_str:
        user.set_weight(weight)

        users_data = get_data_fast(USERS_FILE)
        for user_data in users_data:
            if user_data["id"] == user.get_id():
                user_data["weight"] = weight
                break
        save_data_fast(USERS_FILE, users_data)
    return True