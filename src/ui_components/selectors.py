import streamlit as st
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
    muscles_data = get_data_fast(MUSCLES_FILE)
    muscle_names = [muscle_data["name"].title().replace("_", " ") for muscle_data in muscles_data]

    muscle_name = st.selectbox(
        label="Muscle",
        index=st.session_state["muscle_index"] if st.session_state["muscle_index"] is not None else None,
        accept_new_options=True,
        options=muscle_names)

    muscle = None
    if muscle_name:
        if muscle_name not in muscle_names:
            muscle = Muscle(name=muscle_name.lower().replace(" ", "_"))
            muscles_data.append(muscle.to_json())
            if save_data_fast(MUSCLES_FILE, muscles_data):
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
    exercises_data = get_data_fast(EXERCISES_FILE)
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
            if save_data_fast(EXERCISES_FILE, exercises_data):
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
    workouts_data = get_data_fast(WORKOUTS_FILE)
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
            if save_data_fast(WORKOUTS_FILE, workouts_data):
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

def macrocycle_select(index="macrocycle_index"):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    MACROCYCLES_FILE = check_file(f"{user.get_folder()}/macrocycles.json")
    macrocycles_data = get_data_fast(MACROCYCLES_FILE)
    macrocycle_names = [macrocycle_data["name"].replace("_", " ").title() for macrocycle_data in macrocycles_data]
    if index not in st.session_state:
        st.session_state[index] = None

    macrocycle_name = st.selectbox(
        label="Macrocycle",
        index=st.session_state[index] if st.session_state[index] is not None else None,
        accept_new_options=False,
        options=macrocycle_names
    )

    macrocycle = None
    if macrocycle_name:
        user_microcycles = get_microcycle_list(user=user)
        microcycle_map = {mic.get_id(): mic for mic in user_microcycles}
        for macrocycle_data in macrocycles_data:
            if macrocycle_data["name"] == macrocycle_name.lower().replace(" ", "_"):
                macrocycle = Macrocycle.from_json(macrocycle_data, microcycle_map)
                st.session_state[index] = macrocycle_names.index(macrocycle_name)
                return macrocycle
    return macrocycle

def muscle_multiselect():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    user_muscles = get_muscle_list(user)
    muscle_names = [muscle.get_name().title().replace("_", " ") for muscle in user_muscles]

    if "default_muscles" not in st.session_state:
        st.session_state["default_muscles"] = None

    def handle_change_multiselect():
        st.session_state["default_muscles"] = st.session_state["muscles_multiselect"]

    muscles = st.multiselect(
        label="Muscles",
        placeholder="Select muscles to see their sets",
        accept_new_options=False,
        options=muscle_names,
        default=st.session_state["default_muscles"],
        key="muscles_multiselect",
        on_change=handle_change_multiselect,
        max_selections=6
    )
    return muscles

def category_multiselect():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    user_categories = get_categories_list(user)
    if "default_categories" not in st.session_state:
        st.session_state["default_categories"] = [element for element in ["Arms", "Back", "Chest", "Legs", "Shoulders", "Core"] if element in user_categories]

    def handle_change_multiselect():
        st.session_state["default_categories"] = st.session_state["categories_multiselect"]

    categories = st.multiselect(
        label="Categories",
        accept_new_options=False,
        options=user_categories,
        default=st.session_state["default_categories"],
        key="categories_multiselect",
        on_change=handle_change_multiselect,
        max_selections=None
    )
    return categories

def delta_past_date_selector(session_state):
    if session_state not in st.session_state:
        st.session_state[session_state] = "last week"
    
    options = ["yesterday", "last week", "last month"]

    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    macrocycles = get_macrocycle_list(user=user)
    if len(macrocycles) > 0:
        options.append("start of macrocycle")


    def handle_past_date_select():
        st.session_state[session_state] = st.session_state[f"{session_state}_past_date_selector"]

    past_date = st.selectbox(
        label="Past date",
        label_visibility="collapsed",
        options=options,
        accept_new_options=False,
        index=options.index(st.session_state[session_state]),
        key=f"{session_state}_past_date_selector",
        on_change=handle_past_date_select
    )
    
    return past_date

def main_page_stats_selector():
    if "main_page_stats" not in st.session_state:
        st.session_state["main_page_stats"] = "weight"
    
    options = ["weight", "measurements", "macrocycle"]

    def handle_main_page_stats_select():
        st.session_state["main_page_stats"] = st.session_state["main_page_stats_selector"]

    main_page_stats = st.pills(
        label="Stats:",
        label_visibility="collapsed",
        options=options,
        selection_mode="single",
        default=st.session_state["main_page_stats"],
        key="main_page_stats_selector",
        on_change=handle_main_page_stats_select,
        required=True,
        format_func=lambda x: x.title()
    )
    return main_page_stats

def macrocycle_stats_select():
    if "macrocycle_stats" not in st.session_state:
        st.session_state["macrocycle_stats"] = "general"
    
    options = ["general", "muscle"]

    def handle_macrocycle_stats_select():
        st.session_state["macrocycle_stats"] = st.session_state["macrocycle_stats_selector"]

    macrocycle_stats = st.pills(
        label="Stats:",
        label_visibility="collapsed",
        options=options,
        selection_mode="single",
        default=st.session_state["macrocycle_stats"],
        key="macrocycle_stats_selector",
        on_change=handle_macrocycle_stats_select,
        required=True,
        format_func=lambda x: x.title()
    )
    return macrocycle_stats

def stats_evolution_date_select(index, user_history):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if index not in st.session_state:
        st.session_state[index] = "last 30 days"
    if "custom_range" not in st.session_state:
        st.session_state["custom_range"] = False

    options = ["last week", "last 30 days", "last 90 days", "forever", "custom"]

    macrocycles = get_macrocycle_list(user=user)
    if len(macrocycles) > 0:
        options.insert(-2, "start of macrocycle")

    def handle_date_select():
        st.session_state[index] = st.session_state["stats_evo_date_selector"]
        if st.session_state["stats_evo_date_selector"] == "custom":
            st.session_state["custom_range"] = True
        else:
            st.session_state["custom_range"] = False


    col_selector, col_date = st.columns([0.6,0.4])

    with col_selector:
        past_date = st.selectbox(
            label="Time range:",
            options=options,
            accept_new_options=False,
            index=options.index(st.session_state[index]),
            key="stats_evo_date_selector",
            on_change=handle_date_select,
            format_func=lambda x: x.title()
        )
    with col_date:
        if not user_history:
            min_possible = dt.today().date().strftime('%Y-%m-%d')
            max_possible = min_possible
        else:
            min_possible = user_history[0]["date"]
            max_possible = user_history[-1]["date"]
        custom_date_range = st.date_input(
            label="Custom range:",
            value=(min_possible, max_possible),
            min_value=min_possible,
            max_value=max_possible,
            disabled=(not st.session_state["custom_range"]),
            key="custom_date_range"
        )
    
    return past_date

def measurements_date_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()

    measurements_history = get_measurements_history_list(user=user)
    measurements_dates = [measurement["date"] for measurement in measurements_history]
    measurements_map = {measurement["date"]: measurement for measurement in measurements_history}

    if st.session_state.get("measurements_index", None) is None or st.session_state["measurements_index"] >= len(measurements_dates):
        st.session_state["measurements_index"] = len(measurements_dates) - 1
    
    measurements_date = st.selectbox(
        label="Date",
        index=st.session_state["measurements_index"],
        options=measurements_dates,
    )
    
    measurements = None
    if len(measurements_map) > 0:
        measurements = measurements_map[measurements_date]
    return measurements

def measurements_multiselect():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    user_measurements_history = get_measurements_history_list(user)

    measurement_names = set()
    for entry in user_measurements_history:
        for measurement in entry["measurements"]:
            measurement_names.add(measurement)
    measurement_names = sorted(list(measurement_names))

    if "default_measurements" not in st.session_state:
        st.session_state["default_measurements"] = measurement_names

    def handle_change_multiselect():
        st.session_state["default_measurements"] = st.session_state["measurements_multiselect"]

    measurements = st.multiselect(
        label="Measurements",
        placeholder="Select measurements to compare",
        accept_new_options=False,
        options=measurement_names,
        default=st.session_state["default_measurements"],
        key="measurements_multiselect",
        on_change=handle_change_multiselect,
        format_func=lambda x: x.replace("_", " ").title(),
        max_selections=6
    )
    return measurements

def user_select():
    USERS_FILE = check_file("data/users.json")
    users_data = get_data_fast(USERS_FILE)
    user_ids = [user_data["id"] for user_data in users_data]
    user_id = st.selectbox(
        label="User",
        index=None,
        accept_new_options=False,
        options=user_ids
    )

    user = None
    if user_id:
        for user_data in users_data:
            if user_data["id"] == user_id:
                user = User.from_json(user_data)
                return user
    return user