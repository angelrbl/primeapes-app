import streamlit as st
import json
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.models.Macrocycle import Macrocycle
from src.ui_components.sign_in import is_logged_in
from src.utils.database import *

if "muscle_index" not in st.session_state:
    st.session_state["muscle_index"] = None

if "exercise_index" not in st.session_state:
    st.session_state["exercise_index"] = None

if "workout_index" not in st.session_state:
    st.session_state["workout_index"] = None

if "macrocycle_index" not in st.session_state:
    st.session_state["macrocycle_index"] = None

def muscle_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    muscles_data = load_json_data(MUSCLES_FILE)
    muscle_names = [muscle_data["name"].title().replace("_", " ") for muscle_data in muscles_data]

    muscle_name = st.selectbox(
        label="Muscle",
        index=st.session_state["muscle_index"] if st.session_state["muscle_index"] else None,
        accept_new_options=True,
        options=muscle_names)

    muscle = None
    if muscle_name:
        if muscle_name not in muscle_names:
            muscle = Muscle(name=muscle_name.lower().replace(" ", "_"))
            muscles_data.append(muscle.to_json())
            if save_json_data(MUSCLES_FILE, muscles_data):
                st.session_state["muscle_index"] = len(muscle_names)
                st.rerun()
        else:
            for muscle_json in muscles_data:
                if muscle_json["name"] == muscle_name.lower().replace(" ", "_"):
                    muscle = Muscle.from_json(muscle_json)
                    st.session_state["muscle_index"] = muscle_names.index(muscle_name)
                    return muscle
    return muscle

def exercise_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    EXERCISES_FILE = check_file(f"{user.get_folder()}/exercises.json")
    exercises_data = load_json_data(EXERCISES_FILE)
    exercise_names = [exercise_data["name"].title().replace("_", " ") for exercise_data in exercises_data]

    exercise_name = st.selectbox(
        label="Exercise",
        index=st.session_state["exercise_index"] if st.session_state["exercise_index"] else None,
        accept_new_options=True,
        options=exercise_names)

    exercise = None
    if exercise_name:
        if exercise_name not in exercise_names:
            exercise = Exercise(name=exercise_name.lower().replace(" ", "_"))
            exercises_data.append(exercise.to_json())
            if save_json_data(EXERCISES_FILE, exercises_data):
                st.session_state["exercise_index"] = len(exercise_names)
                st.rerun()
        else:
            user_muscles = get_muscle_list(user=user)
            muscle_map = {m.get_name(): m for m in user_muscles}
            for exercise_data in exercises_data:
                if exercise_data["name"] == exercise_name.lower().replace(" ", "_"):
                    exercise = Exercise.from_json(exercise_data, muscle_map)
                    st.session_state["exercise_index"] = exercise_names.index(exercise_name)
                    return exercise
    return exercise

def workout_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    WORKOUTS_FILE = check_file(f"{user.get_folder()}/workouts.json")
    workouts_data = load_json_data(WORKOUTS_FILE)
    workout_names = [workout_data["name"].replace("_", " ").title() for workout_data in workouts_data]

    workout_name = st.selectbox(
        label="Workout",
        index=st.session_state["workout_index"] if st.session_state["workout_index"] else None,
        accept_new_options=True,
        options=workout_names)


    workout = None
    if workout_name:
        if workout_name not in workout_names:
            workout = Workout(name=workout_name.lower().replace(" ", "_"))
            workouts_data.append(workout.to_json())
            if save_json_data(WORKOUTS_FILE, workouts_data):
                st.session_state["workout_index"] = len(workout_names)
                st.rerun()
        else:
            user_exercises = get_exercise_list(user=user)
            exercise_map = {ex.get_name(): ex for ex in user_exercises}
            for workout_data in workouts_data:
                if workout_data["name"] == workout_name.lower().replace(" ", "_"):
                    workout = Workout.from_json(workout_data, exercise_map)
                    st.session_state["workout_index"] = workout_names.index(workout_name)
                    return workout
    return workout

def macrocycle_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    MACROCYCLES_FILE = check_file(f"{user.get_folder()}/macrocycles.json")
    macrocycles_data = load_json_data(MACROCYCLES_FILE)
    macrocycle_names = [macrocycle_data["name"].replace("_", " ").title() for macrocycle_data in macrocycles_data]
    macrocycle_name = st.selectbox(
        label="Macrocycle",
        index=st.session_state["macrocycle_index"] if st.session_state["macrocycle_index"] else None,
        accept_new_options=False,
        options=macrocycle_names
    )

    macrocycle = None
    if macrocycle_name:
        user_microcycles = get_microcycle_list(user=user)
        microcycle_map = {mic.get_id(): mic for mic in user_microcycles}
        for macrocycles_data in macrocycles_data:
            if macrocycles_data["name"] == macrocycle_name.lower().replace(" ", "_"):
                macrocycle = Macrocycle.from_json(macrocycles_data, microcycle_map)
                st.session_state["macrocycle_index"] = macrocycle_names.index(macrocycle_name)
                return macrocycle
    return macrocycle

