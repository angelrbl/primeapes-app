import streamlit as st
from src.models.Workout import Workout

def workout_total_stat_card(workout, stat, unit=""):
    exercises = workout.get_exercises()

    if not exercises:
        st.metric(label=stat.title(), value=0)

    if stat not in exercises[0]:
        st.error(f"The stat {stat} does not exist on the exercises.")
        return
    
    total = sum(Workout.get_exercise_stat_value(ex, stat) for ex in exercises)

    st.metric(
        label=f"{stat.title()} ({unit})" if unit else stat.title(),
        value=total,
        border=True
    )