import streamlit as st
from src.ui_components.sign_in import is_logged_in
from src.ui_components.cards import weight_card, height_card
from src.ui_components.dialogues import weigh_in_dialog, set_height_dialog

st.set_page_config(page_title="Primeapes", page_icon=":material/exercise:")

is_logged_in()

st.title(f"Welcome, {st.session_state["user"].get_name() if st.session_state["user"] else is_logged_in()}")
st.write("#### These are some of your stats:")

col_weight, col_weight_delta, col_height = st.columns(3, gap="small")

with col_weight:
    weight_card()
    if st.button("Register new weight", width="stretch"):
        weigh_in_dialog()

with col_height:
    height_card()
    if st.button("Update height", width="stretch"):
        set_height_dialog()