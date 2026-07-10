import streamlit as st
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.models.Macrocycle import Macrocycle
from src.models.User import User
from src.ui_components.sign_in import is_logged_in
from src.utils.database import *

def muscle_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if "muscle_index" not in st.session_state:
        st.session_state["muscle_index"] = None
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
    if "exercise_index" not in st.session_state:
        st.session_state["exercise_index"] = None
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
    if "workout_index" not in st.session_state:
        st.session_state["workout_index"] = None
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

def microcycle_select(macrocycle):
    if "selected_week" not in st.session_state or st.session_state["selected_week"] >= macrocycle.get_length():
        st.session_state["selected_week"] = 0
    
    for week_index in range(macrocycle.get_length()):
        is_active = st.session_state["selected_week"] == week_index
        button_type = "primary" if is_active else "secondary"

        if st.button(label=f"Week {week_index + 1}", key=f"week_button_{week_index}", type=button_type, width="stretch"):
            st.session_state["selected_week"] = week_index
            st.rerun()

def macrocycle_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if "macrocycle_index" not in st.session_state:
        st.session_state["macrocycle_index"] = None
    MACROCYCLES_FILE = check_file(f"{user.get_folder()}/macrocycles.json")
    macrocycles_data = load_json_data(MACROCYCLES_FILE)
    macrocycle_names = [macrocycle_data["name"].replace("_", " ").title() for macrocycle_data in macrocycles_data]
    macrocycle_name = st.selectbox(
        label="Macrocycle",
        index=st.session_state["macrocycle_index"] if st.session_state["macrocycle_index"] is not None else None,
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

def category_multiselect():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    user_categories = get_categories_list(user)
    if "default_categories" not in st.session_state:
        st.session_state["default_categories"] = [element for element in ["Arm", "Back", "Chest", "Legs", "Shoulder", "Core"] if element in user_categories]

    def handle_change_multiselect():
        st.session_state["default_categories"] = st.session_state["categories_multiselect"]

    categories = st.multiselect(
        label="Categories",
        accept_new_options=False,
        options=user_categories,
        default=st.session_state["default_categories"],
        key="categories_multiselect",
        on_change=handle_change_multiselect,
        max_selections=6
    )
    return categories

def user_select():
    USERS_FILE = check_file("data/users.json")
    users_data = load_json_data(USERS_FILE)
    user_ids = [user_data["user_id"] for user_data in users_data]
    user_id = st.selectbox(
        label="User",
        index=None,
        accept_new_options=False,
        options=user_ids
    )

    user = None
    if user_id:
        for user_data in users_data:
            if user_data["user_id"] == user_id:
                user = User.from_json(user_data)
                return user
    return user