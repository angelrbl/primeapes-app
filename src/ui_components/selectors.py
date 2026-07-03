import streamlit as st
import json
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.ui_components.sign_in import is_logged_in
from src.utils.database import get_muscle_list, get_exercise_list

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
                st.rerun()
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
                st.rerun()
        else:
            user_muscles = get_muscle_list(user=user)
            muscle_map = {m.get_name(): m for m in user_muscles}
            for exercise_data in exercises_data:
                if exercise_data["name"] == exercise_name.lower().replace(" ", "_"):
                    exercise = Exercise.from_json(exercise_data, muscle_map)
                    return exercise
    return exercise

def workout_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    WORKOUTS_FILE = check_file(f"{user.get_folder()}/workouts.json")
    with open(WORKOUTS_FILE, "r") as f:
        workouts_data = json.load(f)
    workout_names = [workout_data["name"].replace("_", " ").title() for workout_data in workouts_data]

    workout_name = st.selectbox(label="Workout", index=None, accept_new_options=True, options=workout_names)

    workout = None
    if workout_name:
        if workout_name not in workout_names:
            workout = Workout(name=workout_name.lower().replace(" ", "_"))
            workouts_data.append(workout.to_json())
            with open(WORKOUTS_FILE, "w") as f:
                json.dump(workouts_data, f)
                st.rerun()
        else:
            user_exercises = get_exercise_list(user=user)
            exercise_map = {e.get_name(): e for e in user_exercises}
            for workout_data in workouts_data:
                if workout_data["name"] == workout_name.lower().replace(" ", "_"):
                    workout = Workout.from_json(workout_data, exercise_map)
                    return workout
    return workout

#IDEA st.session_state para recordar el índice y si es nuevo el indice es len(x_names) para así que index=st.session_state y evitar bug