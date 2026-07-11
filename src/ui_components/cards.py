import streamlit as st
from src.models.Workout import Workout
from src.ui_components.sign_in import is_logged_in

def workout_total_stat_card(workout, stat, unit=""):
    exercises = workout.get_exercises()

    if not exercises:
        st.metric(
            label=f"{stat.title()} ({unit})" if unit else stat.title(),
            value=0,
            border=True
        )
        return

    if stat not in exercises[0]:
        st.error(f"The stat {stat} does not exist on the exercises.")
        return
    
    total = sum(Workout.get_exercise_stat_value(ex, stat) for ex in exercises)

    st.metric(
        label=f"{stat.title()} ({unit})" if unit else stat.title(),
        value=total,
        border=True
    )

def weight_card():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    
    st.metric(
        label="Bodyweight (kg)",
        value=user.get_weight(),
        border=True
    )

def height_card():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    st.metric(
        label="Height (cm)",
        value=user.get_height(),
        border=True
    )