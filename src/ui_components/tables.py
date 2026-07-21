import streamlit as st
from src.models.Muscle import Muscle
from src.models.Exercise import Exercise
from src.models.Workout import Workout
from src.ui_components.sign_in import is_logged_in
from src.utils.database import *
from math import ceil

def muscle_table(muscle):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not muscle:
        return
    MUSCLES_FILE = check_file(f"{user.get_folder()}/muscles.json")
    table_data = [
        {"Muscle": muscle.get_name().title().replace("_", " "), "Categories": muscle.get_categories()}
    ]

    edited_data = st.data_editor(
        data=table_data, key=f"{muscle.get_name()}_table", hide_index=True, disabled=["Muscle"],
        column_config={
            "Categories": st.column_config.MultiselectColumn(
                "Categories",
                help="Muscle group categories",
                options=muscle.get_categories(),
                format_func=lambda x: x.replace("_", " ").capitalize(),
                accept_new_options=True
            )
        }
    )

    col1, col2 = st.columns(2, gap="small")
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="muscle_save_button", width="stretch"):
        muscles_data = get_data_fast(MUSCLES_FILE)
        if muscle.set_categories(edited_data[0]["Categories"]):
            for i in range(len(muscles_data)):
                if muscle.get_name() == muscles_data[i]["name"]:
                    muscles_data[i] = muscle.to_json()
            save_data_fast(MUSCLES_FILE, muscles_data)
    #DELETE
    if col2.button("Delete muscle", icon=":material/delete:", key="muscle_delete_button", width="stretch"):
        muscles_data = get_data_fast(MUSCLES_FILE)
        for muscle_json in muscles_data:
            if muscle.get_name() == muscle_json["name"]:
                muscles_data.remove(muscle_json)
        if save_data_fast(MUSCLES_FILE, muscles_data):
            st.session_state["muscle_index"] = None
            st.rerun()

def exercise_table(exercise):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not exercise:
        return
    EXERCISES_FILE = check_file(f"{user.get_folder()}/exercises.json")
    table_data = [
        {
            "Exercise": exercise.get_name().replace("_", " ").title(),
            "Primary muscles": exercise.get_primary_muscles_names(),
            "Secondary muscles": exercise.get_secondary_muscles_names()
        }
    ]

    edited_data = st.data_editor(
        data=table_data, key=f"{exercise.get_name()}_table", hide_index=True, disabled=["Exercise"],
        column_config={
            "Primary muscles": st.column_config.MultiselectColumn(
                "Primary muscles",
                help="Exercise's primary muscles",
                options=Muscle.to_name_list(get_muscle_list(user)),
                format_func=lambda x: x.capitalize().replace("_", " ")
            ),
            "Secondary muscles": st.column_config.MultiselectColumn(
                "Secondary muscles",
                help="Exercise's secondary muscles",
                options=Muscle.to_name_list(get_muscle_list(user)),
                format_func=lambda x: x.capitalize().replace("_", " ")
            )
        }
    )

    col1, col2 = st.columns(2, gap="small")
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="exercise_save_button", width="stretch"):
        exercises_data = get_data_fast(EXERCISES_FILE)

        user_muscles = get_muscle_list(user)
        muscle_map = {m.get_name(): m for m in user_muscles}
        primary_muscles = [muscle_map[name] for name in edited_data[0]["Primary muscles"] if name in muscle_map]
        secondary_muscles = [muscle_map[name] for name in edited_data[0]["Secondary muscles"] if name in muscle_map]

        exercise.set_primary_muscles(muscles_list=primary_muscles)
        exercise.set_secondary_muscles(muscles_list=secondary_muscles)

        for i in range(len(exercises_data)):
            if exercise.get_name() == exercises_data[i]["name"]:
                exercises_data[i] = exercise.to_json()
        save_data_fast(EXERCISES_FILE, exercises_data)
    #DELETE
    if col2.button("Delete exercise", icon=":material/delete:", key="exercise_delete_button", width="stretch"):
        exercises_data = get_data_fast(EXERCISES_FILE)
        for exercise_data in exercises_data:
            if exercise.get_name() == exercise_data["name"]:
                exercises_data.remove(exercise_data)
        if save_data_fast(EXERCISES_FILE, exercises_data):
            st.session_state["exercise_index"] = None
            st.rerun() 

def workout_table(workout):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not workout:
        return
    if len(get_exercise_list(user)) == 0:
        st.warning("There are no exercises to build a workout with, please, create some exercises first.")
        return
    WORKOUTS_FILE = check_file(f"{user.get_folder()}/workouts.json")

    user_exercises = get_exercise_list(user)
    exercise_muscles_map = {ex.get_name(): ex.get_primary_muscles_names() for ex in user_exercises}
    exercise_options = Exercise.to_name_list(user_exercises)

    state_key = f"{workout.get_name()}_table_data"

    if state_key not in st.session_state:
        exercises = workout.get_exercises()

        #IF THERE ARE NO EXERCISES IN YOUR WORKOUT (IT IS A NEW WORKOUT), IT INITIALIZES AN EMPTY ENTRY SO THERE IS DATA ON TABLE_DATA
        if len(exercises) != 0:
            table_data = [
                {
                    "exercise": item["exercise"].get_name(),
                    "sets": item["sets"],
                    "reps": item["reps"],
                    "muscles": Muscle.to_name_list(item["muscles"]),
                    "note": item["note"]
                } for item in exercises
            ]
        else:
            table_data = [
                {   
                    "exercise": None,
                    "sets": 3,
                    "reps": "8-12",
                    "muscles": [],
                    "note": ""
                }
            ]

        st.session_state[state_key] = table_data

    user_muscles = Muscle.to_name_list(get_muscle_list(user=user))

    edited_data = st.data_editor(
        data=st.session_state[state_key], key=f"{workout.get_name()}_table", hide_index=True, num_rows="dynamic", disabled=["muscles"],
        column_config={
            "exercise": st.column_config.SelectboxColumn(
                "Exercise",
                help="User's exercises",
                options=exercise_options,
                format_func=lambda x: x.capitalize().replace("_", " "),
                required=True,
                default=None
            ),
            "sets": st.column_config.NumberColumn("Sets", min_value=1, step=1, default=3),
            "reps": st.column_config.TextColumn("Reps", default="8-12"),
            "muscles": st.column_config.MultiselectColumn(
                "Muscles",
                help="Exercise's primary muscles",
                options=user_muscles,
                format_func=lambda x: x.capitalize().replace("_", " ")
            ),
            "note": st.column_config.TextColumn("Note", default="")
    })

    rerun_needed = False

    if len(edited_data) != len(st.session_state[state_key]):
        rerun_needed = True

    for exercise in edited_data:
        expected_muscles = exercise_muscles_map.get(exercise["exercise"], [])
        if exercise["muscles"] != expected_muscles:
            exercise["muscles"] = expected_muscles
            rerun_needed = True

    if rerun_needed:
        st.session_state[state_key] = edited_data
        st.rerun()

    col1, col2 = st.columns(2)
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="workout_save_button", width="stretch"):
        workouts_data = get_data_fast(WORKOUTS_FILE)
        exercise_map = {ex.get_name(): ex for ex in user_exercises}
        edited_exercises = [
            Workout.exercise_from_json(exercise_data=exercise_data, exercise_map=exercise_map) for exercise_data in edited_data
        ]
        workout.set_exercises(edited_exercises)

        for i in range(len(workouts_data)):
            if workout.get_name() == workouts_data[i]["name"]:
                workouts_data[i] = workout.to_json()
        save_data_fast(WORKOUTS_FILE, workouts_data)
    #DELETE
    if col2.button("Delete workout", icon=":material/delete:", key="workout_delete_button", width="stretch"):
        workouts_data = get_data_fast(WORKOUTS_FILE)
        for workout_data in workouts_data:
            if workout.get_name() == workout_data["name"]:
                workouts_data.remove(workout_data)
        save_data_fast(WORKOUTS_FILE, workouts_data)
        if state_key in st.session_state:
            del st.session_state[state_key]
            st.session_state["workout_index"] = None
            st.rerun()

def microcycle_table(microcycle):
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    if not microcycle:
        return
    MICROCYCLE_FILE = check_file(f"{user.get_folder()}/microcycles.json")

    user_workouts = get_workout_list(user)
    workout_options = Workout.to_name_list(user_workouts)

    workouts = microcycle.get_workouts()
    table_data = [{}]
    column_config = {}
    for i in range(len(workouts)):
        table_data[0][f"day_{i}"] = workouts[i].get_name() if workouts[i] is not None else None
        column_config[f"day_{i}"] = st.column_config.SelectboxColumn(
                f"Day {i+1}",
                help="User's workouts",
                options=workout_options,
                format_func=lambda x: x.capitalize().replace("_", " "),
                default=None,
        )
    
    edited_data = st.data_editor(
        data=table_data, key=f"{microcycle.get_id()}_table", hide_index=True, num_rows="fixed",
        column_config=column_config,
        height="content",
        row_height=50,
        placeholder=""
    )

    note = st.text_input(
        label="Note",
        label_visibility="collapsed",
        key=f"{microcycle.get_id()}_note",
        placeholder="Type any special notes for this microcycle.",
        value=microcycle.get_note()
    )

    col_save, col_clear = st.columns(2)
    #SAVE
    if col_save.button(label="Save changes",icon=":material/save:", key="microcycle_save_button", width="stretch"):
        microcycles_data = get_data_fast(MICROCYCLE_FILE)
        workout_map = {wrk.get_name(): wrk for wrk in user_workouts}
        
        for day, workout_name in edited_data[0].items():
            microcycle.set_workout(workout_map[workout_name] if workout_name is not None else None, int(day.split("_")[1]))

        if note:
            microcycle.set_note(note)

        for i in range(len(microcycles_data)):
            if microcycle.get_id() == microcycles_data[i]["id"]:
                microcycles_data[i] = microcycle.to_json()
        if save_data_fast(MICROCYCLE_FILE, microcycles_data):
            st.rerun()
    #DELETE
    if col_clear.button(label="Clear Workouts",icon=":material/delete:", key="microcycle_clear_button", width="stretch"):
        microcycles_data = get_data_fast(MICROCYCLE_FILE)

        microcycle.clear_workouts()

        for i in range(len(microcycles_data)):
            if microcycle.get_id() == microcycles_data[i]["id"]:
                microcycles_data[i] = microcycle.to_json()
        if save_data_fast(MICROCYCLE_FILE, microcycles_data):
            st.rerun()

def macrocycle_table(macrocycle):
    if not macrocycle:
        return
    
    if not "first_microcycle" in st.session_state or not "last_microcycle" in st.session_state:
        st.session_state["first_microcycle"] = 0
        st.session_state["last_macrocycle"] = 4

    if macrocycle.get_length() <= 4:
        pagination_needed = False
        st.session_state["first_microcycle"] = 0
        st.session_state["last_microcycle"] = macrocycle.get_length()
    else:
        pagination_needed = True

    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    MICROCYCLE_FILE = check_file(f"{user.get_folder()}/microcycles.json")

    table_data = []
    columns_config = {
        "week": st.column_config.TextColumn(
            label="",
            help="Week number",
            alignment="center"
        )
    }
    
    for i in range(st.session_state["first_microcycle"], st.session_state["last_microcycle"]):
        table_data.append({})
        microcycle = macrocycle.get_microcycle(i)
        workouts = microcycle.get_workouts()
        table_data[i - st.session_state["first_microcycle"]]["week"] = f"Week {i + 1}"
        for j in range(len(workouts)):
                table_data[i - st.session_state["first_microcycle"]][f"day_{j}"] = workouts[j].get_name().replace("_", " ").title() if workouts[j] is not None else None
    for k in range(len(table_data[0].keys())):
        columns_config[f"day_{k}"] = st.column_config.TextColumn(
                    f"Day {k+1}",
                    help="User's workouts per microcycle",
                    alignment="center"
            )         

    st.dataframe(
        data=table_data, key=f"{microcycle.get_id()}_table", hide_index=True,
        column_config=columns_config,
        height="content",
        row_height=85,
        placeholder=""
    )
    col_pagination, col_clear = st.columns([0.7,0.3], vertical_alignment="center")
    with col_pagination:
        if pagination_needed:
            total_pages = int(ceil(macrocycle.get_length() / 4))
            current_page_index = (st.session_state["first_microcycle"] // 4 + 1)

            def handle_page_change():
                selected_page = st.session_state["macrocycle_pagination"] - 1
                st.session_state["first_microcycle"] = selected_page * 4
                st.session_state["last_microcycle"] = selected_page * 4 + 4

            st.pagination(
                total_pages,
                default=current_page_index,
                key="macrocycle_pagination",
                on_change=handle_page_change
            )
    with col_clear:
        if col_clear.button(label="Clear Workouts",icon=":material/delete:", key="macrocycle_clear_button", width="stretch"):
            microcycles_data = get_data_fast(MICROCYCLE_FILE)

            macrocycle.clear_microcycles()

            for microcycle in macrocycle.get_microcycles():
                microcycle.set_note("")
                for i in range(len(microcycles_data)):
                    if microcycle.get_id() == microcycles_data[i]["id"]:
                        microcycles_data[i] = microcycle.to_json()
            if save_data_fast(MICROCYCLE_FILE, microcycles_data):
                st.rerun()

def measurements_table(measurements_data):
    if measurements_data is None:
        return
    user = st.session_state["user"] if st.session_state["user"] else is_logged_in()
    MEASUREMENTS_HISTORY_FILE = check_file(f"{user.get_folder()}/measurements_history.json")
    USERS_FILE = "data/users.json"

    measurements = measurements_data["measurements"]
    table_data = []
    
    if not measurements:
        table_data.append({"body_part": None, "measure": None})

    for body_part, measure in measurements.items():
        table_data.append({"body_part": body_part.replace("_", " ").title(), "measure": measure})

    edited_data = st.data_editor(
        data=table_data,
        column_config={
            "measure": st.column_config.NumberColumn(
                "Measure (cm)",
                help="Measure of the body part in cm",
                min_value=0,
                step=0.1,
                alignment="center"
            ),
            "body_part": st.column_config.TextColumn(
                label="Body Part",
                alignment="center",
                required=True
            )
        },
        hide_index=True,
        num_rows="dynamic"
    )
    
    edited_measurements = {}
    for measurement in edited_data:
        if measurement["body_part"]:
            edited_measurements[measurement["body_part"].lower().replace(" ", "_")] = measurement["measure"]
        
    col1, col2 = st.columns(2, gap="small")
    #SAVE
    if col1.button("Save changes", icon=":material/save:", key="muscle_save_button", width="stretch"):
        user_measurements_data = get_data_fast(MEASUREMENTS_HISTORY_FILE)
        for i in range(len(user_measurements_data)):
            if user_measurements_data[i]["date"] == measurements_data["date"]:
                user_measurements_data[i]["measurements"] = edited_measurements
        save_data_fast(MEASUREMENTS_HISTORY_FILE, user_measurements_data)
        if user_measurements_data[-1]["date"] == measurements_data["date"]:
            user.set_measurements(edited_measurements)
            users_data = get_data_fast(USERS_FILE)
            for i in range(len(users_data)):
               if users_data[i]["id"] == user.get_id():
                   users_data[i] = user.to_json()
                   break
            save_data_fast(USERS_FILE, users_data)
    #DELETE
    if col2.button("Delete measurements", icon=":material/delete:", key="muscle_delete_button", width="stretch"):
        user_measurements_data = get_data_fast(MEASUREMENTS_HISTORY_FILE)
        if user_measurements_data[-1]["date"] == measurements_data["date"]:
            previous_data = user_measurements_data[-2] if len(user_measurements_data) > 1 else {}
            user.set_measurements(previous_data)
            users_data = get_data_fast(USERS_FILE)
            for i in range(len(users_data)):
               if users_data[i]["id"] == user.get_id():
                   users_data[i] = user.to_json()
                   break
            save_data_fast(USERS_FILE, users_data)

        updated_measurements = [m for m in user_measurements_data if m["date"] != measurements_data["date"]]
        if save_data_fast(MEASUREMENTS_HISTORY_FILE, updated_measurements):
            st.session_state["measurements_index"] = len(user_measurements_data) - 1

        st.rerun()