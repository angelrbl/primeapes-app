import streamlit as st
from src.utils.auth import *
from src.ui_components.dialogues import new_user_dialog

def log_in():
    #LOG IN
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "new_user_data" not in st.session_state:
        st.session_state["new_user_data"] = False

    if not st.session_state["logged_in"]:
        st.title("Primeapes")
        st.subheader("Please, log in or make a new account.")
        tab1, tab2 = st.tabs(["Sign in", "Sign up"])
        with tab1:
            st.write("###### Introduce a valid user and password: ")
            username = st.text_input(label="Username", placeholder="Type a valid username", key="login_user", value="")
            password = st.text_input(label="Password", placeholder="Type a valid password", key="login_password", type="password", value="")

            if st.button("Log in", key="log_in_button"):
                if check_credentials(username=username, password=password):
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = initialize_user(username)
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with tab2:
            st.write("###### Introduce a valid user and password: ")
            new_username = (st.text_input(label="Username", placeholder="Type a valid username", key="signin_user", value="").lower().replace(" ", "_"))
            new_password = (st.text_input(label="Password", placeholder="Type a valid password", key="signin_password", type="password", value=""))

            if st.button("Create account", key="create_account_button"):
                if new_username and new_password:
                    if create_user_account(username=new_username, password=new_password):
                        st.session_state["new_user_data"] = False
                        if not st.session_state["new_user_data"]:
                            new_user_dialog()
                            st.stop()
                    else:
                        st.error("This username already exists, try another one.")
                else:
                    st.error("Invalid username or password")
            if st.session_state["new_user_data"]:
                initialize_new_user(user_id=new_username, name=st.session_state["new_user_data"]["name"], weight=st.session_state["new_user_data"]["weight"], height=st.session_state["new_user_data"]["height"])
                st.session_state["new_user_data"] = False
                st.success("Your account was successfully created! Now, please log in.")

        if st.session_state["logged_in"] == False:
            st.stop()

def log_out():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.rerun()

def is_logged_in():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] == False:
        log_in()

    st.sidebar.write(f"Logged in as: **{st.session_state["user"].get_id()}**")
    if st.sidebar.button("Log out"):
        log_out()

    return st.session_state["logged_in"]