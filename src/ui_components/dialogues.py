import streamlit as st
from src.models.Macrocycle import Macrocycle
from src.utils.files import check_file
import json

@st.dialog("Create new user", dismissible=False)
def new_user_dialog():
    name = st.text_input(label="Name", placeholder="Type your name", key="new_user_name")
    weight = st.number_input(label="Weight", placeholder="Type your weight (kg)", key="new_user_weight", value=None, step=1)
    height = st.number_input(label="Height", placeholder="Type your height (cm)", key="new_user_height", value=None, step=1)
    if st.button("Create user"):
        if not (name and weight and height):
            st.error("Please, fill all the items before submitting.")
        else:
            st.session_state["new_user_data"] = {"name": name, "weight": weight, "height": height}
            st.rerun()

@st.dialog("Add new macrocycle")
def add_macrocycle_dialog():
    col1, col2 = st.columns([0.8, 0.2])
    name = col1.text_input(label="Name", placeholder="Macrocycle name", key="add_macrocycle_name")
    start_date = col2.date_input(label="Starting date", value="today", key="add_macrocycle_start_date")
    description = st.text_area(label="Description", placeholder="A description for your macrocycle", key="add_¨macrocycle_description")
    length = st.number_input(label="Lenght", placeholder="Num of microcycles in your plan", min_value=1, key="add_macrocycle_length")

    if st.button("Add macrocycle", width="stretch"):
        if not name:
            st.error("Please, introduce a name for your Macrocycle.")
        else:
            # FUTURO SAVE_CHANGES GENERALIZADO??
            user = st.session_state["user"]
            MACROCYCLES_FILE = check_file(f"{user.get_folder()}/macrocycles.json")
            with open(MACROCYCLES_FILE, "r") as f:
                macrocycles_data = json.load(f)
            macrocycle = Macrocycle(name=name, start_date=start_date, description=description, length=length)
            macrocycles_data.append(macrocycle.to_json())
            with open(MACROCYCLES_FILE, "w") as f:
                json.dump(macrocycles_data, f, default=str)
                st.session_state["macrocycle_index"] = len(macrocycles_data) - 1
                st.rerun()