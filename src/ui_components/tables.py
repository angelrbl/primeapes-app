import streamlit as st
import json
from src.models.Muscle import Muscle
from src.ui_components.sign_in import is_logged_in

def muscle_table(muscle):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not muscle:
        st.info("Please select a muscle to view its categories.")
        return
    MUSCLES_FILE = f"{user.get_folder()}/muscles.json"
    table_data = [
        {"Muscle": muscle.get_name().title(), "Categories": muscle.categories_to_string()}
    ]
    #CONVERTIR CATEGORIES EN MULTISELECT COLUMN
    edited_data = st.data_editor(data=table_data, key=f"{muscle.get_name()}_table", hide_index=True, disabled=["Muscle"])
    col1, col2 = st.columns(2, gap="small")
    #SAVE
    if col1.button("Save changes", icon=":material/save:"):
        with open(MUSCLES_FILE, 'r') as f:
            muscles_data = json.load(f)
        categories = Muscle.categories_to_list(edited_data[0]["Categories"])
        muscle.set_categories(categories)
        for i in range(len(muscles_data)):
            if muscle.get_name() == muscles_data[i]["name"]:
                muscles_data[i] = muscle.to_json()
        with open(MUSCLES_FILE, 'w') as f:
            json.dump(muscles_data, f)
    #DELETE
    if col2.button("Delete muscle", icon=":material/delete:"):
        with open(MUSCLES_FILE, 'r') as f:
            muscles_data = json.load(f)
        for muscle_json in muscles_data:
            if muscle.get_name() == muscle_json["name"]:
                muscles_data.remove(muscle_json)
        with open(MUSCLES_FILE, 'w') as f:
            json.dump(muscles_data, f)
            st.rerun()