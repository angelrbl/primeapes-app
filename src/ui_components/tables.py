import streamlit as st
import json
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.ui_components.sign_in import is_logged_in
from src.utils.database import *

def muscle_table(muscle):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not muscle:
        return
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    table_data = [
        {"Muscle": muscle.get_name().title(), "Categories": muscle.get_categories()}
    ]

    edited_data = st.data_editor(
        data=table_data, key=f"{muscle.get_name()}_table", hide_index=True, disabled=["Muscle"],
        column_config={
            "Categories": st.column_config.MultiselectColumn(
                "Categories",
                help="Muscle group categories",
                options=muscle.get_categories(),
                format_func=lambda x: x.capitalize( ),
                accept_new_options=True
            )
        }
    )

    col1, col2 = st.columns(2, gap="small")
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="muscle_save_button", width="stretch"):
        with open(MUSCLES_FILE, 'r') as f:
            muscles_data = json.load(f)
        muscle.set_categories(edited_data[0]["Categories"])
        for i in range(len(muscles_data)):
            if muscle.get_name() == muscles_data[i]["name"]:
                muscles_data[i] = muscle.to_json()
        with open(MUSCLES_FILE, 'w') as f:
            json.dump(muscles_data, f)
    #DELETE
    if col2.button("Delete muscle", icon=":material/delete:", key="muscle_delete_button", width="stretch"):
        with open(MUSCLES_FILE, 'r') as f:
            muscles_data = json.load(f)
        for muscle_json in muscles_data:
            if muscle.get_name() == muscle_json["name"]:
                muscles_data.remove(muscle_json)
        with open(MUSCLES_FILE, 'w') as f:
            json.dump(muscles_data, f)
            st.rerun()

def exercise_table(exercise):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not exercise:
        return
    EXERCISES_FILE = check_file(f"{user.get_folder()}/exercises.json")
    table_data = [
        {
            "Exercise": exercise.get_name().replace("_", " ").title(),
            "Primary muscles": exercise.get_primary_muscles_names(),
            "Secondary muscles": exercise.get_secondary_muscles_names()
        }
    ]

    edited_data = st.data_editor(
        data=table_data, key=f"{exercise.get_name()}_table", hide_index=True, disabled=["Exercise"],
        column_config={
            "Primary muscles": st.column_config.MultiselectColumn(
                "Primary muscles",
                help="Exercise's primary muscles",
                options=Muscle.to_name_list(get_muscle_list(user)),
                format_func=lambda x: x.capitalize()
            ),
            "Secondary muscles": st.column_config.MultiselectColumn(
                "Secondary muscles",
                help="Exercise's secondary muscles",
                options=Muscle.to_name_list(get_muscle_list(user)),
                format_func=lambda x: x.capitalize()
            )
        }
    )

    col1, col2 = st.columns(2, gap="small")
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="exercise_save_button", width="stretch"):
        with open(EXERCISES_FILE, 'r') as f:
            exercises_data = json.load(f)

        user_muscles = get_muscle_list(user)
        muscle_map = {m.get_name(): m for m in user_muscles}
        primary_muscles = [muscle_map[name] for name in edited_data[0]["Primary muscles"] if name in muscle_map]
        secondary_muscles = [muscle_map[name] for name in edited_data[0]["Secondary muscles"] if name in muscle_map]

        exercise.set_primary_muscles(muscles_list=primary_muscles)
        exercise.set_secondary_muscles(muscles_list=secondary_muscles)

        for i in range(len(exercises_data)):
            if exercise.get_name() == exercises_data[i]["name"]:
                exercises_data[i] = exercise.to_json()
        with open(EXERCISES_FILE, 'w') as f:
            json.dump(exercises_data, f)
    #DELETE
    if col2.button("Delete exercise", icon=":material/delete:", key="exercise_delete_button", width="stretch"):
        with open(EXERCISES_FILE, 'r') as f:
            exercises_data = json.load(f)
        for exercise_data in exercises_data:
            if exercise.get_name() == exercise_data["name"]:
                exercises_data.remove(exercise_data)
        with open(EXERCISES_FILE, 'w') as f:
            json.dump(exercises_data, f)    
            st.rerun() 

def workout_table(workout):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not workout:
        return
    if len(get_exercise_list(user)) == 0:
        st.warning("There are no exercises to build a workout with, please, create some exercises first.")
        return
    WORKOUTS_FILE = check_file(f"{user.get_folder()}/workouts.json")

    user_exercises = get_exercise_list(user)
    exercise_muscles_map = {ex.get_name(): ex.get_primary_muscles_names() for ex in user_exercises}
    exercise_options = Exercise.to_name_list(user_exercises)

    state_key = f"{workout.get_name()}_table_data"

    if state_key not in st.session_state:
        exercises = workout.get_exercises()

        #IF THERE ARE NO EXERCISES IN YOUR WORKOUT (IT IS A NEW WORKOUT), IT INITIALIZES AN EMPTY ENTRY SO THERE IS DATA ON TABLE_DATA
        if len(exercises) != 0:
            table_data = [
                {
                    "exercise": item["exercise"].get_name(),
                    "sets": item["sets"],
                    "reps": item["reps"],
                    "muscles": Muscle.to_name_list(item["muscles"]),
                    "note": item["note"]
                } for item in exercises
            ]
        else:
            table_data = [
                {   
                    "exercise": None,
                    "sets": 3,
                    "reps": "8-12",
                    "muscles": [],
                    "note": ""
                }
            ]

        st.session_state[state_key] = table_data


    edited_data = st.data_editor(
        data=st.session_state[state_key], key=f"{workout.get_name()}_table", hide_index=True, num_rows="dynamic", disabled=["muscles"],
        column_config={
            "exercise": st.column_config.SelectboxColumn(
                "Exercise",
                help="User's exercises",
                options=exercise_options,
                format_func=lambda x: x.capitalize().replace("_", " "),
                required=True,
                default=None
            ),
            "sets": st.column_config.NumberColumn("Sets", min_value=1, step=1, default=3),
            "reps": st.column_config.TextColumn("Reps", default="8-12"),
            "muscles": st.column_config.MultiselectColumn(
                "Muscles",
                help="Exercise's primary muscles",
                format_func=lambda x: x.capitalize().replace("_", " ") if x else ""
            ),
            "note": st.column_config.TextColumn("Note", default="")
    })

    rerun_needed = False

    if len(edited_data) != len(st.session_state[state_key]):
        rerun_needed = True

    for exercise in edited_data:
        expected_muscles = exercise_muscles_map.get(exercise["exercise"], [])
        if exercise["muscles"] != expected_muscles:
            exercise["muscles"] = expected_muscles
            rerun_needed = True

    if rerun_needed:
        st.session_state[state_key] = edited_data
        st.rerun()

    col1, col2 = st.columns(2)
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="workout_save_button", width="stretch"):
        with open(WORKOUTS_FILE, 'r') as f:
            workouts_data = json.load(f)
        exercise_map = {ex.get_name(): ex for ex in user_exercises}
        edited_exercises = [
            Workout.exercise_from_json(exercise_data=exercise_data, exercise_map=exercise_map) for exercise_data in edited_data
        ]
        workout.set_exercises(edited_exercises)

        for i in range(len(workouts_data)):
            if workout.get_name() == workouts_data[i]["name"]:
                workouts_data[i] = workout.to_json()
        with open(WORKOUTS_FILE, 'w') as f:
            json.dump(workouts_data, f)
    #DELETE
    if col2.button("Delete workout", icon=":material/delete:", key="workout_delete_button", width="stretch"):
        with open(WORKOUTS_FILE, 'r') as f:
            workouts_data = json.load(f)
        for workout_data in workouts_data:
            if workout.get_name() == workout_data["name"]:
                workouts_data.remove(workout_data)
        with open(WORKOUTS_FILE, 'w') as f:
            json.dump(workouts_data, f)    
        if state_key in st.session_state:
            del st.session_state[state_key]
            st.rerun()

def microcycle_table(microcycle):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not microcycle:
        return
    if len(get_workout_list(user)) == 0:
        st.warning("There are no workouts to build a microcycle with, please, create some exercises first.")
        return
    MICROCYCLE_FILE = check_file(f"{user.get_folder()}/microcycles.json")