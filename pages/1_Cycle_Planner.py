import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.selectors import macrocycle_select
from src.ui_components.dialogues import add_macrocycle_dialog

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
st.title("Cycle Planner")
st.write("###### Select a macrocycle or create a new one:")

col1, col2 = st.columns([0.7, 0.3], vertical_alignment="bottom")
with col1:
    macrocycle = macrocycle_select()
with col2:
    st.button("Add new", on_click=add_macrocycle_dialog)