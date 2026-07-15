import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.cards import weight_card, height_card, weight_delta_card
from src.ui_components.dialogues import weigh_in_dialog, set_height_dialog
from src.ui_components.selectors import bodyweight_past_date_selector, main_page_stats_selector, weight_evolution_date_selector
from src.ui_components.charts import weight_evolution_chart
from src.ui_components.forms import edit_weight_evolution_form

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()

st.title(f"Welcome, {st.session_state["user"].get_name() if st.session_state["user"] else is_logged_in()}.")
st.space("small")
st.write("#### These are some of your stats:")

#GENERAL STATS
col_weight, col_weight_delta, col_height = st.columns(3, gap="small", vertical_alignment="top")

with col_weight:
    weight_card()
    if st.button("Register new weight", width="stretch"):
        weigh_in_dialog()

with col_weight_delta:
    if "bodyweight_past_date" not in st.session_state:
        st.session_state["bodyweight_past_date"] = "last week"
    weight_delta_card(st.session_state["bodyweight_past_date"])
    bodyweight_past_date_selector()

with col_height:
    height_card()
    if st.button("Update height", width="stretch"):
        set_height_dialog()

st.space("small")
st.divider()
st.space("small")

#SPECIFIC STATS
main_page_stats_selector()
st.space("small")

match st.session_state["main_page_stats"]:
    case "weight":
        st.write("##### Bodyweight evolution")
        time_range = weight_evolution_date_selector()
        weight_evolution_chart(time_range=time_range)

        edit_button_container = st.container(horizontal_alignment="right")
        if edit_button_container.button(label="Edit entries", icon=":material/edit:"):
            st.session_state["show_edit_weight_evo_form"] = not st.session_state.get("show_edit_weight_evo_form", False)
        
        if st.session_state.get("show_edit_weight_evo_form") == True:
            edit_weight_evolution_form()