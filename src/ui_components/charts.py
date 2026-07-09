import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

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
            'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top' # Centramos el título
        },
        xaxis_title=None,
        yaxis_title="Total sets",
        margin=dict(l=20, r=20, t=60, b=20),
        height=250 + (len(df) * 25), # Altura dinámica: se estira si hay muchos músculos
        paper_bgcolor="rgba(0,0,0,0)", # Fondo exterior transparente (se adapta a modo oscuro/claro)
        plot_bgcolor="rgba(0,0,0,0)",  # Fondo interior del gráfico transparente
    )

    st.plotly_chart(fig, width="content", config={"displayModeBar": False})