import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from src.utils.database import get_categories_dict, get_bodyweight_history_list, get_muscle_list, get_macrocycle_list
from src.ui_components.sign_in import is_logged_in
from src.models.Muscle import Muscle
from datetime import datetime as dt, timedelta

def muscle_volume_chart(muscle_sets):
    if not muscle_sets:
        return

    df = pd.DataFrame(data=muscle_sets.items(), columns=["Muscle", "Sets"])
    df = df.sort_values(by="Sets", ascending=True)

    fig = px.bar(
        data_frame=df,
        x="Muscle",
        y="Sets",
        orientation="v",
        text="Sets"
    )

    fig.update_traces(
        marker_color="#FF4B4B",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        title={
            'text': "Volume by Muscle Group",
            'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        xaxis_title=None,
        yaxis_title="Total sets",
        margin=dict(l=20, r=20, t=60, b=20),
        height=250 + (len(df) * 25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, width="content", config={"displayModeBar": False})

def microcycles_muscle_volume_chart(microcycles_muscle_sets, selected_muscles = []):
    if not microcycles_muscle_sets:
        return
    if len(selected_muscles) == 0:
        user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
        selected_muscles = [muscle.get_name().replace("_", "0").title() for muscle in get_muscle_list(user=user)]

    df = pd.DataFrame(microcycles_muscle_sets)

    filtered_df = df[df["Muscle"].isin(selected_muscles)]

    fig = px.bar(
        filtered_df,
        x="Microcycle",
        y="Sets",
        color="Muscle",
        barmode="group",
        height=400,
        labels={"Sets": "Sets", "Microcycle": "Microcycles", "Muscle": "Muscle Group"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        margin=dict(l=20,r=20,t=30, b=20),
        xaxis_title=None,
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

def category_volume_chart(selected_categories, muscle_sets):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    categories_sets_map = get_categories_dict(user=user)
    categories_sets = Muscle.get_category_sets(category_map=categories_sets_map, muscle_sets=muscle_sets)

    categories = []
    volume_sets = []

    for category in selected_categories:
        categories.append(category)
        if category in categories_sets.keys():
            volume_sets.append(categories_sets[category])
        else:
            volume_sets.append(0)


    bar_width = ([0.96] * len(categories)) if len(categories) > 0 else ([0.96]*6)

    fig = go.Figure(go.Barpolar(
        r=volume_sets,
        theta=categories,
        width=bar_width,
        marker_color="#FF4B4B",
        marker_line_color="#131722",
        marker_line_width=2,
        opacity=0.85,
        hoverinfo="theta+r"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=30, l=30, r=30),
        polar=dict(
            angularaxis=dict(
                direction="clockwise",
                period=len(categories) if len(categories) > 0 else 6,
                gridcolor="rgba(255, 255, 255, 0.1)",
                ticks=""
            ),
            radialaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.1)",
                showticklabels=True,
                tickfont=dict(color="rgba(255, 255, 255, 0.5)")
            )
        )
    )

    st.plotly_chart(fig, width="content", config={"displayModeBar": False})

def weight_evolution_chart(time_range):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    user_bodyweight_history = get_bodyweight_history_list(user=user)
    user_macrocycles = get_macrocycle_list(user=user)
    if len(user_macrocycles) > 0:
        selected_macrocycle = user_macrocycles[st.session_state.get("macrocycle_stats_index", -1)]

    if len(user_bodyweight_history) == 0:
        st.info("Not enough data to show user's bodyweight evolution.")
        return

    df = pd.DataFrame(user_bodyweight_history)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df.sort_values("date")

    today = dt.today().date()
    filtered_df = df.copy()

    match(time_range):
        case "last week":
            filtered_df = df[df["date"] >= (today - timedelta(days=7))]
        case "last 30 days":
            filtered_df = df[df["date"] >= (today - timedelta(days=30))]
        case "last 90 days":
            filtered_df = df[df["date"] >= (today - timedelta(days=90))]
        case "start of macrocycle":
            filtered_df = df[df["date"] >= (dt.strptime(selected_macrocycle.get_start_date(), '%Y-%m-%d').date())]
        case "custom":
            if "custom_date_range" not in st.session_state:
                st.session_state["custom_date_range"] = (df["date"].min(), df["date"].max())
            custom_date_range = st.session_state["custom_date_range"]
            if isinstance(custom_date_range, tuple) and len(custom_date_range) == 2:
                start_date, end_date = custom_date_range
                filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    
    if filtered_df.empty:
        st.info("Not enough data to show user's bodyweight evolution.")
        return

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df["date"],
        y=filtered_df["weight"],
        mode="lines+markers",
        line=dict(color="#FF4B4B", width=3),
        marker=dict(size=7, color="#FF4B4B"),
        hovertemplate="Date: %{x}, Weight: %{y} kg"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, color="rgba(255,255,255,0.6)", tickformat="%d %b"),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)", color="rgba(255,255,255,0.6)", autorange=True)
    )

    st.plotly_chart(fig, width="content", config={"displayModeBar": False})