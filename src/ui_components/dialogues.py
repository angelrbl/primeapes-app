import streamlit as st
from src.models.Macrocycle import Macrocycle
from src.utils.files import check_file
from src.utils.database import save_json_data, load_json_data, add_weigh_in, get_bodyweight_history_list
from src.utils.auth import delete_user
from src.ui_components.selectors import user_select
from math import ceil
from datetime import datetime as dt

@st.dialog("Create new user", dismissible=False)
def new_user_dialog():
    name = st.text_input(label="Name", placeholder="Type your name", key="new_user_name")
    weight = st.number_input(label="Weight", placeholder="Type your weight (kg)", key="new_user_weight", value=None, step=0.01, min_value=1.0)
    height = st.number_input(label="Height", placeholder="Type your height (cm)", key="new_user_height", value=None, step=0.1, min_value=1.0)
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
            for macrocycle_data in macrocycles_data:
                if macrocycle_data["name"] == name.lower().replace(" ", "_"):
                    st.error("This name is already used by another macrocycle, please try another one.")
                    st.stop()
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

@st.dialog("Weigh in")
def weigh_in_dialog():
    st.write("Register your bodyweight:")
    col_weight, col_date = st.columns([0.7, 0.3])
    weight = col_weight.number_input(label="Weight (kg)", min_value=1.0, placeholder="Enter a valid weight (kg)", key="new_weight_input", value=None, step=0.01)
    date = col_date.date_input(label="Date", value="today", key="weigh_date_input")

    if st.button("Register weight", width="stretch"):
        if not weight:
            st.error("Please, enter a valid weight")
        else:
            user = st.session_state["user"]
            add_weigh_in(user=user, weight=weight, date=date)
            st.rerun()

def edit_weight_evolution_dialog():
    user = st.session_state["user"]
    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    user_bodyweight_history = get_bodyweight_history_list(user=user)
    reversed_bodyweight_history = list(reversed(user_bodyweight_history))

    custom_date_range = st.date_input(
            label="Custom range:",
            value=(reversed_bodyweight_history[-1]["date"], reversed_bodyweight_history[0]["date"]),
            min_value=reversed_bodyweight_history[-1]["date"],
            max_value=reversed_bodyweight_history[0]["date"],
            key="edit_bodyweight_custom_range"
    )
    #CREATE FILTERED BODYWEIGHT HISTORY
    if isinstance(custom_date_range, tuple) and len(custom_date_range) == 2:
        start_date = custom_date_range[0]
        end_date = custom_date_range[1]
        filtered_bodyweight_history = []
        for entry in reversed_bodyweight_history:
            entry_date = dt.strptime(entry["date"], '%Y-%m-%d').date()
            if entry_date >= start_date and entry_date <= end_date:
                filtered_bodyweight_history.append(entry)
    else:
        filtered_bodyweight_history = reversed_bodyweight_history

    st.divider()
    items_per_page = 8

    total_items = len(filtered_bodyweight_history)
    total_pages = ceil(total_items / items_per_page) if ceil(total_items / items_per_page) > 0 else 1

    bodyweight_table = [st.empty() for _ in range(items_per_page + 1)]
    
    
    #PAGINATION
    active_page = st.pagination(num_pages=total_pages, width="stretch", key="weight_history_pagination")

    start_index = (active_page - 1) * items_per_page
    end_index = start_index + items_per_page
    page_items = filtered_bodyweight_history[start_index:end_index]

    if len(page_items) == 0:
        st.info("There are no entries in the selected date range.")

    #TABLE TITLE
    col_title_date, col_title_weight, col_3, col_4 = bodyweight_table[0].columns([3, 3, 1, 1], vertical_alignment="center")
    col_title_date.write("**Date**")
    col_title_weight.write("**Weight**")

    for index, entry in enumerate(page_items):
        date = entry["date"]
        weight = entry["weight"]

        row_key = f"{date}_{start_index + index}"

        is_editing = st.session_state.get("editing_weight_date") == date

        col_date, col_weight, col_btn1, col_btn2 = bodyweight_table[index + 1].columns([3, 3, 1, 1], vertical_alignment="center")

        if is_editing:
            col_date.write(f"**{date}**")
            new_weight = col_weight.number_input(
                label="Edit weight value",
                min_value=float(1.0),
                value=weight,
                step=0.1,
                label_visibility="collapsed",
                key=f"input_weight_{row_key}"
            )
            if col_btn1.button(label="", icon=":material/check:", key=f"save_weight_{row_key}", help="Save changes", type="primary"):
                for original_entry in user_bodyweight_history:
                    if original_entry["date"] == date:
                        original_entry["weight"] = new_weight
                        if original_entry["date"] == user_bodyweight_history[-1]["date"]:
                            user.set_weight(new_weight)
                        break
                save_json_data(BODYWEIGHT_HISTORY_FILE, user_bodyweight_history)
                st.session_state["editing_weight_date"] = None
                st.rerun()
            if col_btn2.button(label="", icon=":material/close:", key=f"cancel_weight_{row_key}", help="Cancel"):
                st.session_state["editing_weight_date"] = None
                st.rerun()
        else:
            col_date.write(f"**{date}**")
            col_weight.write(f"{weight} kg")
            if col_btn1.button(label="", icon=":material/edit:", key=f"edit_btn_{row_key}", help="Edit weight"):
                st.session_state["editing_weight_date"] = date
                st.rerun()
            with col_btn2.popover(label="", icon=":material/delete:", help="Delete entry"):
                st.write("Delete record?")
                if st.button("Yes, delete", key=f"confirm_delete_{row_key}", type="primary"):
                    updated_bodyweight_history = [item for item in user_bodyweight_history if item["date"] != date]
                    if updated_bodyweight_history[-1]["date"] != user_bodyweight_history[-1]["date"]:
                        user.set_weight(updated_bodyweight_history[-1]["weight"])
                    save_json_data(BODYWEIGHT_HISTORY_FILE, updated_bodyweight_history)
                    st.rerun()
        
    if st.button("Save changes and close", width="stretch", key="save_and_close_edit_bodyweight_evo"):
        st.session_state["show_edit_weight_evo_dialog"] = False
        st.rerun()

@st.dialog("Edit height")
def set_height_dialog():
    st.write("Update your height:")
    height = st.number_input(label="Height", placeholder="Enter a valid height (cm)", key="set_height_input", value=None, step=0.1, min_value=1.0)

    if st.button("Update height", width="stretch"):
        if not height:
            st.error("Please, enter a valid height")
        else:
            USERS_FILE = check_file(f"data/users.json")
            user = st.session_state["user"]
            user.set_height(height=height)

            users_data = load_json_data(USERS_FILE)
            for user_data in users_data:
                if user_data["id"] == user.get_id():
                    user_data["height"] = height
                    break
            save_json_data(USERS_FILE, users_data)
            st.rerun()