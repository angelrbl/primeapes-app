import streamlit as st
import json

def muscle_select():
    MUSCLES_FILE = "data/muscles.json"
    with open(MUSCLES_FILE, "r") as f:
        muscles_data = json.load(f)
    muscle_jsons = [muscle_json for muscle_json in muscles_data["muscles"]]
    muscle_names = [muscle["name"].title() for muscle in muscle_jsons]
    muscle_name = st.selectbox(label="Muscle", index=None, accept_new_options=True, options=muscle_names)
    muscle_json = None
    if muscle_name and muscle_name not in muscle_names:
        muscle_json = {
            "name": muscle_name.lower(),
            "categories": []
        }
        muscles_data["muscles"].append(muscle_json)
        with open(MUSCLES_FILE, "w") as f:
            json.dump(muscles_data, f)
    elif muscle_name:
        for muscle in muscle_jsons:
            if muscle["name"] == muscle_name.lower():
                muscle_json = muscle 
    return muscle_json