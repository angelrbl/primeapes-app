import streamlit as st
from src.utils.database import get_bodyweight_history_list, save_json_data
from src.utils.files import check_file
from math import ceil
from datetime import datetime as dt


def edit_weight_evolution_form():
    user = st.session_state["user"]
    BODYWEIGHT_HISTORY_FILE = check_file(f"{user.get_folder()}/bodyweight_history.json")
    user_bodyweight_history = get_bodyweight_history_list(user=user)
    reversed_bodyweight_history = list(reversed(user_bodyweight_history))

    with st.container(key="edit_weight_evolution_form", border=True):
        st.subheader("Edit bodyweight evolution")

        custom_date_range = st.date_input(
                label="Custom range:",
                value=(reversed_bodyweight_history[-1]["date"], reversed_bodyweight_history[0]["date"]),
                min_value=reversed_bodyweight_history[-1]["date"],
                max_value=reversed_bodyweight_history[0]["date"],
                key="edit_bodyweight_custom_range"
        )
        #CREATE FILTERED BODYWEIGHT HISTORY
        if isinstance(custom_date_range, tuple) and len(custom_date_range) == 2:
            start_date = custom_date_range[0]
            end_date = custom_date_range[1]
            filtered_bodyweight_history = []
            for entry in reversed_bodyweight_history:
                entry_date = dt.strptime(entry["date"], '%Y-%m-%d').date()
                if entry_date >= start_date and entry_date <= end_date:
                    filtered_bodyweight_history.append(entry)
        else:
            filtered_bodyweight_history = reversed_bodyweight_history

        st.divider()
        items_per_page = 8

        total_items = len(filtered_bodyweight_history)
        total_pages = ceil(total_items / items_per_page) if ceil(total_items / items_per_page) > 0 else 1

        bodyweight_table = [st.empty() for _ in range(items_per_page + 1)]
        
        
        #PAGINATION
        active_page = st.pagination(num_pages=total_pages, width="stretch", key="weight_history_pagination")

        start_index = (active_page - 1) * items_per_page
        end_index = start_index + items_per_page
        page_items = filtered_bodyweight_history[start_index:end_index]

        if len(page_items) == 0:
            st.info("There are no entries in the selected date range.")

        #TABLE TITLE
        col_title_date, col_title_weight, col_3, col_4 = bodyweight_table[0].columns([3, 3, 1, 1], vertical_alignment="center")
        col_title_date.write("**Date**")
        col_title_weight.write("**Weight**")

        for index, entry in enumerate(page_items):
            date = entry["date"]
            weight = entry["weight"]

            row_key = f"{date}_{start_index + index}"

            is_editing = st.session_state.get("editing_weight_date") == date

            col_date, col_weight, col_btn1, col_btn2 = bodyweight_table[index + 1].columns([3, 3, 1, 1], vertical_alignment="center")

            if is_editing:
                col_date.write(f"**{date}**")
                new_weight = col_weight.number_input(
                    label="Edit weight value",
                    min_value=float(1.0),
                    value=weight,
                    step=0.1,
                    label_visibility="collapsed",
                    key=f"input_weight_{row_key}"
                )
                if col_btn1.button(label="", icon=":material/check:", key=f"save_weight_{row_key}", help="Save changes", type="primary"):
                    for original_entry in user_bodyweight_history:
                        if original_entry["date"] == date:
                            original_entry["weight"] = new_weight
                            if original_entry["date"] == user_bodyweight_history[-1]["date"]:
                                user.set_weight(new_weight)
                            break
                    save_json_data(BODYWEIGHT_HISTORY_FILE, user_bodyweight_history)
                    st.session_state["editing_weight_date"] = None
                    st.rerun()
                if col_btn2.button(label="", icon=":material/close:", key=f"cancel_weight_{row_key}", help="Cancel"):
                    st.session_state["editing_weight_date"] = None
                    st.rerun()
            else:
                col_date.write(f"**{date}**")
                col_weight.write(f"{weight} kg")
                if col_btn1.button(label="", icon=":material/edit:", key=f"edit_btn_{row_key}", help="Edit weight"):
                    st.session_state["editing_weight_date"] = date
                    st.rerun()
                with col_btn2.popover(label="", icon=":material/delete:", help="Delete entry"):
                    st.write("Delete record?")
                    if st.button("Yes, delete", key=f"confirm_delete_{row_key}", type="primary"):
                        updated_bodyweight_history = [item for item in user_bodyweight_history if item["date"] != date]
                        if updated_bodyweight_history[-1]["date"] != user_bodyweight_history[-1]["date"]:
                            user.set_weight(updated_bodyweight_history[-1]["weight"])
                        save_json_data(BODYWEIGHT_HISTORY_FILE, updated_bodyweight_history)
                        st.rerun()
            
        if st.button("Save changes and close", width="stretch", key="save_and_close_edit_bodyweight_evo"):
            st.session_state["show_edit_weight_evo_form"] = False
            st.rerun()