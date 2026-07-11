import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.selectors import workout_select, category_multiselect
from src.ui_components.tables import workout_table
from src.ui_components.cards import workout_total_stat_card
from src.ui_components.charts import muscle_volume_chart, category_volume_chart

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
st.title("Workout Tracker")
st.write("Please, select a workout or create a new one: ")

workout = workout_select()
if not workout:
    st.stop()

st.write(f"Showing your workout - **{workout.get_name().title().replace("_", " ")}**:")
workout_table(workout)
st.space("small")
st.write("### Workout stats:")
col1, col2, col3 = st.columns(3)
with col1:
    workout_total_stat_card(workout=workout, stat="exercise")
with col2:
    workout_total_stat_card(workout=workout, stat="sets")
with col3:
    workout_total_stat_card(workout=workout, stat="reps", unit="aprox")

col_polar_chart, col_bar_chart = st.columns([0.4,0.6], vertical_alignment="center")
muscle_sets = workout.get_muscle_sets()
with col_polar_chart:
    if muscle_sets is not None:
        categories = category_multiselect()
        category_volume_chart(selected_categories=categories, muscle_sets=muscle_sets)
with col_bar_chart:
    muscle_volume_chart(muscle_sets=muscle_sets)
    