import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.selectors import macrocycle_select, microcycle_select
from src.ui_components.dialogues import add_macrocycle_dialog
from src.ui_components.tables import microcycle_table

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
st.title("Cycle Planner")
st.write("###### Select a macrocycle or create a new one:")

col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")
with col1:
    macrocycle = macrocycle_select()
with col2:
    st.button("Add new", on_click=add_macrocycle_dialog, width="stretch")

if not macrocycle:
   st.stop()

# Show basic data from your macrocycle
col1, col2 = st.columns([0.7, 0.3])
col1.write(f"###### Showing - {macrocycle.get_name().title().replace("_", " ")}")
col2.write(f"###### Starting date: {macrocycle.get_date()}")
description = macrocycle.get_description()
if description:
    with st.expander(label="Description"):
        st.write(description)

st.divider()
# Microcycle
col_selector, col_table = st.columns([1, 5], gap="small")
with col_selector:
    with st.container(height=220, border=False):
        microcycle_select(macrocycle=macrocycle)
with col_table:
    if "selected_week" in st.session_state:
        microcycle_table(macrocycle.get_microcycle(st.session_state["selected_week"]))