import streamlit as st
import json

def muscle_table(muscle_json):
    if not muscle_json:
        st.info("Please select a muscle to view its categories.")
        return
    MUSCLES_FILE = "data/muscles.json"
    for i in range(len(muscle_json["categories"])):
        muscle_json["categories"][i] = muscle_json["categories"][i].title().replace("_", " ")
    categories_string = ", ".join(muscle_json["categories"])
    table_data = [
        {"Muscle": muscle_json["name"].title(), "Categories": categories_string}
    ]
    edited_data = st.data_editor(data=table_data, key=f"{muscle_json["name"]}_table", hide_index=True, disabled=["Muscle"])
    col1, col2 = st.columns(2, gap="small")
    if col1.button("Save changes", icon=":material/save:"):
        with open(MUSCLES_FILE, 'r') as f:
            muscles_data = json.load(f)
        categories = edited_data[0]["Categories"].split(", ")
        for i in range(len(categories)):
            categories[i] = categories[i].lower().replace(" ", "_")
        for muscle in muscles_data["muscles"]:
            if muscle["name"] == muscle_json["name"]:
                muscle["categories"] = categories
        with open(MUSCLES_FILE, 'w') as f:
            json.dump(muscles_data, f)
    if col2.button("Delete muscle", icon=":material/delete:"):
        ...