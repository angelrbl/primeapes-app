import streamlit as st
import json
from src.utils.files import check_file
from src.models.Muscle import Muscle
from src.ui_components.sign_in import is_logged_in

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
    if col1.button("Save changes", icon=":material/save:", key="muscle_save_button"):
        with open(MUSCLES_FILE, 'r') as f:
            muscles_data = json.load(f)
        muscle.set_categories(edited_data[0]["Categories"])
        for i in range(len(muscles_data)):
            if muscle.get_name() == muscles_data[i]["name"]:
                muscles_data[i] = muscle.to_json()
        with open(MUSCLES_FILE, 'w') as f:
            json.dump(muscles_data, f)
    #DELETE
    if col2.button("Delete muscle", icon=":material/delete:", key="muscle_delete_button"):
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
            "Primary muscles": exercise.get_primary_muscles(),
            "Secondary muscles": exercise.get_secondary_muscles()
        }
    ]

    edited_data = st.data_editor(
        data=table_data, key=f"{exercise.get_name()}_table", hide_index=True, disabled=["Exercise"],
        column_config={
            "Primary muscles": st.column_config.MultiselectColumn(
                "Primary muscles",
                help="Exercise's primary muscles",
                options=Muscle.to_list(Muscle.get_name_list(user)),
                format_func=lambda x: x.capitalize()
            ),
            "Secondary muscles": st.column_config.MultiselectColumn(
                "Secondary muscles",
                help="Exercise's secondary muscles",
                options=Muscle.to_list(Muscle.get_name_list(user)),
                format_func=lambda x: x.capitalize()
            )
        }
    )

    col1, col2 = st.columns(2, gap="small")
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="exercise_save_button"):
        with open(EXERCISES_FILE, 'r') as f:
            exercises_data = json.load(f)
        exercise.set_primary_muscles(muscles_list=edited_data[0]["Primary muscles"], user=user)
        exercise.set_secondary_muscles(muscles_list=edited_data[0]["Secondary muscles"], user=user)
        for i in range(len(exercises_data)):
            if exercise.get_name() == exercises_data[i]["name"]:
                exercises_data[i] = exercise.to_json()
        with open(EXERCISES_FILE, 'w') as f:
            json.dump(exercises_data, f)
    #DELETE
    if col2.button("Delete muscle", icon=":material/delete:", key="exercise_delete_button"):
        with open(EXERCISES_FILE, 'r') as f:
            exercises_data = json.load(f)
        for exercise_data in exercises_data:
            if exercise.get_name() == exercise_data["name"]:
                exercises_data.remove(exercise_data)
        with open(EXERCISES_FILE, 'w') as f:
            json.dump(exercises_data, f)    
        st.rerun() 