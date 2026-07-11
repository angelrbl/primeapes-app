import streamlit as st

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

pg = st.navigation([
    st.Page(page="pages/main_page.py", title="Main Page", icon=":material/home:"),
    st.Page(page="pages/cycle_planner.py", title="Cycle Planner", icon=":material/calendar_month:"),
    st.Page(page="pages/workout_tracker.py", title="Workout Tracker", icon=":material/avg_pace:"),
    st.Page(page="pages/exercise_database.py", title="Exercise Database", icon=":material/fitness_center:")]
)

pg.run()