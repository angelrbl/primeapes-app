import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from src.utils.database import get_categories_dict
from src.ui_components.sign_in import is_logged_in
from src.models.Muscle import Muscle

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

    print(categories)
    print(volume_sets)

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