import streamlit as st

@st.dialog("Create new user")
def new_user_dialog():
    st.write("###### Create new user:")
    name = st.text_input(label="Name", placeholder="Type your name", key="new_user_name")
    weight = st.number_input(label="Weight", placeholder="Type your weight (kg)", key="new_user_weight", value=None, step=1)
    height = st.number_input(label="Height", placeholder="Type your height (cm)", key="new_user_height", value=None, step=1)
    if st.button("Create user"):
        if not (name and weight and height):
            st.error("Please, fill all the items before submitting.")
        else:
            st.session_state["new_user_data"] = {"name": name, "weight": weight, "height": height}
            st.rerun()