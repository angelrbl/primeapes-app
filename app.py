import streamlit as st
from src.ui_components.sign_in import is_logged_in

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()

st.title(f"Welcome, {st.session_state["username"]}")