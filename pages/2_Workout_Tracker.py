import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.selectors import workout_select
from src.ui_components.tables import workout_table
from src.ui_components.cards import workout_total_stat_card
from src.ui_components.charts import workout_volume_chart

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()
st.title("Workout Tracker")
st.write("Please, select a workout or create a new one: ")

workout = workout_select()
if workout:
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
    
    workout_volume_chart(workout)
    