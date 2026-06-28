import streamlit as st
from src.utils.auth import *

def log_in():
    #LOG IN
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.title("Primeapes")
        st.subheader("Please, log in or make a new account.")
        tab1, tab2 = st.tabs(["Sign in", "Sign up"])
        with tab1:
            st.write("###### Introduce a valid user and password: ")
            username = st.text_input(label="Username", placeholder="Type a valid username", key="login_user", value="")
            password = st.text_input(label="Password", placeholder="Type a valid password", key="login_password", type="password", value="")

            if st.button("Log in"):
                if check_credentials(username=username, password=password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with tab2:
            st.write("###### Introduce a valid user and password: ")
            new_username = (st.text_input(label="Username", placeholder="Type a valid username", key="signin_user", value="").lower().replace(" ", "_"))
            new_password = (st.text_input(label="Password", placeholder="Type a valid password", key="signin_password", type="password", value=""))

            if st.button("Create account"):
                if create_user_account(username=new_username, password=new_password):
                    st.success("Your account was successfully created! Now, please log in.")
                else:
                    st.error("This username already exists, try another one.")

        if st.session_state["logged_in"] == False:
            st.stop()

def log_out():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.rerun()

def is_logged_in():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] == False:
        log_in()

    st.sidebar.write(f"Logged in as: **{st.session_state["username"]}**")
    if st.sidebar.button("Log out"):
        log_out()

    return st.session_state["logged_in"]