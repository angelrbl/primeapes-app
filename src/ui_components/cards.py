import streamlit as st
from src.models.Workout import Workout
from src.ui_components.sign_in import is_logged_in
from src.utils.database import get_bodyweight_history_list
from datetime import datetime as dt, timedelta as td
from math import ceil

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
        value=f"{user.get_weight()} kg",
        border=True
    )

def height_card():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    st.metric(
        label="Height (cm)",
        value=f"{user.get_height()} cm",
        border=True
    )

def weight_delta_card(past_date):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    past_date_map = {
        "yesterday": 1,
        "last week": 7,
        "last month": 30
    }
    margin_map = {
        "yesterday": 1,
        "last week": 3,
        "last month": 5
    }
    num_of_days = margin_map[past_date]
    max_margin_days = margin_map[past_date]

    user_bodyweight_history = get_bodyweight_history_list(user=user)
    last_entry = user_bodyweight_history[-1]
    target_date = dt.strptime(last_entry["date"], '%Y-%m-%d').date() - td(days=num_of_days)

    target_weight = None
    min_diff_days = max_margin_days + 1

    for entry in user_bodyweight_history:
        entry_date = dt.strptime(entry["date"], '%Y-%m-%d').date()
        diff_days = abs((entry_date - target_date).days)

        if diff_days <= max_margin_days and diff_days < min_diff_days:
            min_diff_days = diff_days
            target_weight = entry["weight"]


    value = "N/A"
    delta_value = 0
    if target_weight:
        weight_diff = last_entry["weight"] - target_weight
        if target_weight >= 0:
            value = f"+{weight_diff} kg"
        else:
            value = f"-{weight_diff} kg"
        delta_value = (weight_diff / last_entry["weight"]) * 100

    st.metric(
        label=f"Difference since {past_date}",
        value=value,
        delta=f"{"+" if delta_value >= 0 else "-"}{delta_value:.2f} %",
        border=True
    )