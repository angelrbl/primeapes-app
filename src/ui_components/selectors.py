import streamlit as st
import json
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.ui_components.sign_in import is_logged_in

def muscle_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    with open(MUSCLES_FILE, "r") as f:
        muscles_data = json.load(f)
    muscle_names = [muscle_data["name"].title().replace("_", " ") for muscle_data in muscles_data]

    muscle_name = st.selectbox(label="Muscle", index=None, accept_new_options=True, options=muscle_names)

    muscle = None
    if muscle_name:
        if muscle_name not in muscle_names:
            muscle = Muscle(name=muscle_name.lower().replace(" ", "_"))
            muscles_data.append(muscle.to_json())
            with open(MUSCLES_FILE, "w") as f:
                json.dump(muscles_data, f)
        else:
            for muscle_json in muscles_data:
                if muscle_json["name"] == muscle_name.lower().replace(" ", "_"):
                    muscle = Muscle.from_json(muscle_json)
                    return muscle
    return muscle

def exercise_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    EXERCISES_FILE = check_file(f"{user.get_folder()}/exercises.json")
    with open(EXERCISES_FILE, "r") as f:
        exercises_data = json.load(f)
    exercise_names = [exercise_data["name"].title().replace("_", " ") for exercise_data in exercises_data]

    exercise_name = st.selectbox(label="Exercise", index=None, accept_new_options=True, options=exercise_names)

    exercise = None
    if exercise_name:
        if exercise_name not in exercise_names:
            exercise = Exercise(name=exercise_name.lower().replace(" ", "_"))
            exercises_data.append(exercise.to_json())
            with open(EXERCISES_FILE, "w") as f:
                json.dump(exercises_data, f)
        else:
            for exercise_data in exercises_data:
                if exercise_data["name"] == exercise_name.lower().replace(" ", "_"):
                    exercise = Exercise.from_json(exercise_data, user)
                    return exercise
    return exercise
