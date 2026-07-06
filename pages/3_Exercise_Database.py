import streamlit as st
import json
from src.ui_components.selectors import muscle_select, exercise_select
from src.ui_components.tables import muscle_table, exercise_table
from src.ui_components.sign_in import is_logged_in

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
# EXERCISES
st.title("Exercise Database")
st.write("Please, select an exercise or create a new one: ")
exercise = exercise_select()
exercise_table(exercise)

st.divider()

# MUSCLES
st.title("Muscle Database")
st.write("Please, select a muscle or create a new one: ")
muscle = muscle_select()
muscle_table(muscle)