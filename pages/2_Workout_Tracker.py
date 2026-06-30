import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.selectors import workout_select

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
st.title("Workout Tracker")
st.write("Please, select a workout or create a new one: ")
workout = workout_select()