import streamlit as st
from src.models.Macrocycle import Macrocycle
from src.utils.files import check_file
from src.utils.database import save_json_data, load_json_data
from src.utils.auth import delete_user
from src.ui_components.selectors import user_select

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

@st.dialog("Manage users")
def manage_users_dialog():
    col1, col2 = st.columns([0.03, 0.97], vertical_alignment="bottom")
    col1.write("**@**")
    with col2:
        user = user_select()
    if not user:
        st.stop()
    st.write(f"Do you want to delete the user **@{user.get_id()}** and all its folders and data?")
    if st.button(label="Delete user", key="delete_user_button", icon=":material/delete:", type="primary"):
        delete_user(user)
        st.rerun()
        st.toast(f"You deleted all the data of **@{user.get_id()}**", duration="short")

@st.dialog("Add new macrocycle")
def add_macrocycle_dialog():
    col1, col2 = st.columns([0.7, 0.3])
    name = col1.text_input(label="Name", placeholder="Macrocycle name", key="add_macrocycle_name")
    start_date = col2.date_input(label="Starting date", value="today", key="add_macrocycle_start_date")
    description = st.text_area(label="Description", placeholder="A description for your macrocycle", key="add_¨macrocycle_description")
    col1, col2 = st.columns(2)
    macrocycle_length = col1.number_input(label="Macrocycle length", placeholder="Num of microcycles in your plan", value=None, min_value=1, key="add_macrocycle_length")
    microcycle_length = col2.number_input(label="Microcycle length", placeholder="Num of days in a microcycle", value=None, min_value=1, key="add_microcycle_length")

    if st.button("Add macrocycle", width="stretch"):
        if not (name and microcycle_length and macrocycle_length):
            st.error("Missing essential info to create your Macrocycle.")
        else:
            user = st.session_state["user"]
            #GUARDAMOS MACROCICLO
            MACROCYCLES_FILE = check_file(f"{user.get_folder()}/macrocycles.json")
            macrocycles_data = load_json_data(MACROCYCLES_FILE)
            macrocycle = Macrocycle(
                name=name.lower().replace(" ", "_"),
                start_date=start_date,
                description=description,
                length=macrocycle_length,
                microcycle_length=microcycle_length)
            macrocycles_data.append(macrocycle.to_json())
            save_json_data(MACROCYCLES_FILE, macrocycles_data)
            #GUARDAMOS MICROCICLOS
            MICROCYCLES_FILE = check_file(f"{user.get_folder()}/microcycles.json")
            microcycles_data = load_json_data(MICROCYCLES_FILE)
            for microcycle in macrocycle.get_microcycles():
                microcycles_data.append(microcycle.to_json()) 
            if save_json_data(MICROCYCLES_FILE, microcycles_data):
                st.session_state["macrocycle_index"] = len(macrocycles_data) - 1
                st.rerun()