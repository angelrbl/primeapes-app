import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.selectors import macrocycle_select

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
st.title("Cycle Planner")
col1, col2 = st.columns([0.7, 0.3])
with col1:
    macrocycle = macrocycle_select()