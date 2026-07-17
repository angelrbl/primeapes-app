import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.cards import weight_card, height_card, weight_delta_card,macrocycle_stats_cards
from src.ui_components.dialogues import weigh_in_dialog, set_height_dialog, add_measurements_dialog
from src.ui_components.selectors import bodyweight_past_date_selector, main_page_stats_selector, weight_evolution_date_select
from src.ui_components.selectors import macrocycle_select, macrocycle_stats_select, muscle_multiselect, measurements_date_select
from src.ui_components.charts import weight_evolution_chart, muscle_volume_chart, microcycles_muscle_volume_chart
from src.ui_components.forms import edit_weight_evolution_form
from src.ui_components.tables import measurements_table
from src.utils.database import get_macrocycle_list

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
with st.container(horizontal_alignment="center", vertical_alignment="center"):
    col_text, col_pills = st.columns([0.3,0.7])
    col_text.write("**Stats:**")
    with col_pills:     main_page_stats_selector()
st.divider()

match st.session_state["main_page_stats"]:
    case "weight":
        st.write("##### Bodyweight evolution")
        time_range = weight_evolution_date_select()
        weight_evolution_chart(time_range=time_range)

        edit_button_container = st.container(horizontal_alignment="right")
        if edit_button_container.button(label="Edit entries", icon=":material/edit:"):
            st.session_state["show_edit_weight_evo_form"] = not st.session_state.get("show_edit_weight_evo_form", False)
        
        if st.session_state.get("show_edit_weight_evo_form") == True:
            edit_weight_evolution_form()
    
    case "measurements":
        st.write("##### Measurements")
        col_date, col_add_new = st.columns([0.8,0.2], vertical_alignment="bottom")
        with col_date:
            measurements_data = measurements_date_select()
        with col_add_new:
            if st.button(label="Add new", width="stretch"):
                add_measurements_dialog()
        
        measurements_table(measurements_data=measurements_data)

    case "macrocycle":
        st.write("##### Macrocycle stats")

        macrocycles = get_macrocycle_list(user=st.session_state["user"])
        if not macrocycles:
            st.info("There are no macrocycles to show stats from.")
            st.stop()
        macrocycle = macrocycles[st.session_state.get("macrocycle_stats_index", 0)]

        macrocycle_stats_cards(macrocycle=macrocycle)

        macrocycle_stats_select()
        match st.session_state["macrocycle_stats"]:
            case "general":
                muscle_sets = macrocycle.get_muscle_sets()
                muscle_volume_chart(muscle_sets=muscle_sets)
            case "muscle":
                muscle_sets = macrocycle.get_microcycles_muscle_sets()
                selected_muscles = muscle_multiselect()
                microcycles_muscle_volume_chart(microcycles_muscle_sets=muscle_sets, selected_muscles=selected_muscles)
        
        with st.container(border=True):
            col_text, col_change = st.columns([0.75,0.25], vertical_alignment="center")
            col_text.write(f"Current macrocycle - {macrocycle.get_name().replace("_", " ").title()}")
            popover = col_change.popover(label="Change macrocycle", on_change="rerun")
            with popover:
                if popover.open:
                    if "macrocycle_stats_index" not in st.session_state:
                        st.session_state["macrocycle_stats_index"] = 0
                    new_macrocycle = macrocycle_select(index="macrocycle_stats_index")