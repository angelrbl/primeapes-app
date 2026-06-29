import streamlit as st
import json
from src.ui_components.selectors import muscle_select, exercise_select
from src.ui_components.tables import muscle_table, exercise_table
from src.ui_components.sign_in import is_logged_in

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
# EXERCISES
st.title("Exercise Database")
exercise = exercise_select()
exercise_table(exercise)

# MUSCLES
st.title("Muscle Database")
muscle = muscle_select()
muscle_table(muscle)