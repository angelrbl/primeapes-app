import streamlit as st
from src.models.Workout import Workout
from src.ui_components.sign_in import is_logged_in
from src.utils.database import get_bodyweight_history_list, get_measurements_history_list, get_macrocycle_list
from datetime import datetime as dt, timedelta as td

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

def macrocycle_stats_cards(macrocycle):
    microcycles = macrocycle.get_microcycles()

    workout_amount = sum(microcycle.get_workout_amount() for microcycle in microcycles)

    exercise_amount = 0
    exercise_sets = 0
    exercise_reps = 0
    for microcycle in microcycles:
        microcycle_workouts = microcycle.get_workouts()
        for workout in microcycle_workouts:
            if workout:
                exercise_amount += workout.get_exercise_amount()
                for ex in workout.get_exercises():
                    exercise_sets += Workout.get_exercise_stat_value(ex, "sets")
                    exercise_reps += Workout.get_exercise_stat_value(ex, "reps")

    col1, col2, col3 = st.columns(3, vertical_alignment="top")
    col1.metric(
        label="Microcycles",
        value=f"{macrocycle.get_length()}",
        border=True,
        )
    with col2:
        st.metric(
            label="Workouts",
            value=f"{workout_amount}",
            border=True 
        )
        st.metric(
            label="Exercises",
            value=f"{exercise_amount}",
            border=True 
        )
    with col3:
        st.metric(
            label="Sets",
            value=f"{exercise_sets}",
            border=True 
        )
        st.metric(
            label="Reps (aprox)",
            value=f"{exercise_reps}",
            border=True 
        )

def weight_card():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    
    user_bodyweight_history = get_bodyweight_history_list(user=user)
    bodyweight_history_data = [entry["weight"] for entry in user_bodyweight_history]
    st.metric(
        label="Bodyweight (kg)",
        value=f"{user.get_weight()} kg",
        border=True,
        chart_data=bodyweight_history_data,
        chart_type="line",
        delta_color="blue"
    )

def height_card():
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    st.metric(
        label="Height (cm)",
        value=f"{user.get_height()} cm",
        border=True,
        height="stretch"
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
        "last month": 5,
        "start of macrocycle": 5
    }
    macrocycles = get_macrocycle_list(user=user)
    if len(macrocycles) > 0:
        today = dt.today().date()
        macrocycle_start_date = dt.strptime(macrocycles[st.session_state.get("macrocycle_stats_index", -1)].get_start_date(), '%Y-%m-%d').date()
        past_date_map["start of macrocycle"] = (today - macrocycle_start_date).days

    num_of_days = past_date_map[past_date]
    max_margin_days = margin_map[past_date]

    user_bodyweight_history = get_bodyweight_history_list(user=user)
    if len(user_bodyweight_history) <= 0:
        return
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
        if weight_diff >= 0:
            value = f"+{weight_diff:.2f} kg"
        else:
            value = f"{weight_diff:.2f} kg"
        delta_value = (weight_diff / target_weight) * 100

    st.metric(
        label=f"Difference since {past_date}",
        value=value,
        delta=f"{"+" if delta_value >= 0 else ""}{delta_value:.2f} %",
        height="stretch",
        border=True
    )

def measurements_delta_card(past_date, is_gain, last_entry = None):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    past_date_map = {
        "yesterday": 1,
        "last week": 7,
        "last month": 30
    }
    margin_map = {
        "yesterday": 1,
        "last week": 3,
        "start of macrocycle": 5
    }
    macrocycles = get_macrocycle_list(user=user)
    if len(macrocycles) > 0:
        today = dt.today().date()
        macrocycle_start_date = dt.strptime(macrocycles[st.session_state.get("macrocycle_stats_index", -1)].get_start_date(), '%Y-%m-%d').date()
        past_date_map["start of macrocycle"] = (today - macrocycle_start_date).days

    num_of_days = past_date_map[past_date]
    max_margin_days = margin_map[past_date]

    user_measurements_history = get_measurements_history_list(user=user)
    if len(user_measurements_history) <= 0:
        return
    if not last_entry:
        last_entry = user_measurements_history[-1]
    target_date = dt.strptime(last_entry["date"], '%Y-%m-%d').date() - td(days=num_of_days)

    target_measurements = None
    min_diff_days = max_margin_days + 1

    for entry in user_measurements_history:
        entry_date = dt.strptime(entry["date"], '%Y-%m-%d').date()
        diff_days = abs((entry_date - target_date).days)

        if diff_days <= max_margin_days and diff_days < min_diff_days:
            min_diff_days = diff_days
            target_measurements = entry["measurements"]

    value = ['N/A', 'N/A']
    max_diff = 0
    delta_value = 0
    if target_measurements:
        for body_part, measure in target_measurements.items():
            if not measure:
                measure = 0
            elif body_part in last_entry["measurements"].keys():
                last_measurements = last_entry["measurements"][body_part]
                if not last_measurements:
                    last_measurements = measure
                diff = last_measurements - measure
                if is_gain == False and max_diff >= diff:
                    max_diff = diff
                    value[0] = body_part.replace("_", " ").title()
                    value[1] = f"{diff} cm"
                    delta_value = (max_diff / measure) * 100
                elif is_gain == True and max_diff <= diff:
                    max_diff = diff
                    value[0] = body_part.replace("_", " ").title()
                    value[1] = f"+{diff} cm"
                    delta_value = (max_diff / measure) * 100
    
    st.metric(
        label=f"{value[0]} {'gain' if is_gain is True else 'loss'} since {past_date}",
        value=value[1],
        delta=f"{"+" if is_gain == True else "-"}{delta_value:.2f} %",
        border=True
    )