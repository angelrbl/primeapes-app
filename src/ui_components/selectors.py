import streamlit as st
import json
from src.models.Muscle import Muscle
from src.ui_components.sign_in import is_logged_in

def muscle_select():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    MUSCLES_FILE = f"{user.get_folder()}/muscles.json"
    with open(MUSCLES_FILE, "r") as f:
        muscles_data = json.load(f)
    muscle_names = [muscle_json["name"].title() for muscle_json in muscles_data]
    muscle_name = st.selectbox(label="Muscle", index=None, accept_new_options=True, options=muscle_names, key="muscle_name_select")

    muscle = None
    if muscle_name and muscle_name not in muscle_names:
        muscle = Muscle(name=muscle_name.lower(), categories=[])
        muscles_data.append(muscle.to_json())
        with open(MUSCLES_FILE, "w") as f:
            json.dump(muscles_data, f)
    elif muscle_name:
        for muscle_json in muscles_data:
            if muscle_json["name"] == muscle_name.lower():
                muscle = Muscle.from_json(muscle_json)
                return muscle
    return muscle