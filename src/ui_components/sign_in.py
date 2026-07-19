import streamlit as st
from src.utils.auth import *
from src.utils.database import add_weigh_in

def log_in():
    #LOG IN
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "new_user_data" not in st.session_state:
        st.session_state["new_user_data"] = False

    def switch_tab(tab):
        st.session_state.log_in_tabs = tab
    
    if not st.session_state["logged_in"]:
        st.title("Primeapes.")
        st.subheader("Please, log in or make a new account.")
        tab1, tab2 = st.tabs([":material/login: Log in", ":material/for_you: Sign up"], key="log_in_tabs", default=":material/login: Log in", on_change="rerun")
        with tab1:
            st.write("###### Introduce a valid user and password: ")
            username = st.text_input(label="Username", placeholder="Type a valid username", key="login_user", value="", icon=":material/account_circle:")
            password = st.text_input(label="Password", placeholder="Type a valid password", key="login_password", type="password", value="", icon=":material/password:")

            st.space("small")
            col_login, col_signup = st.columns(2, gap="small")
            if col_login.button("Log in", key="log_in_button", icon=":material/login:", width="stretch"):
                if check_credentials(username=username, password=password):
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = initialize_user(username)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            col_signup.button("Sign up", key="go_to_sign_up_button", icon=":material/for_you:", on_click=switch_tab, args=(":material/for_you: Sign up",), width="stretch")

        with tab2:
            st.write("###### Introduce a valid user and password: ")
            new_username = (st.text_input(label="Username", placeholder="Type a valid username", key="signin_user", value="", icon=":material/account_circle:").lower().replace(" ", "_"))
            new_password = (st.text_input(label="Password", placeholder="Type a valid password", key="signin_password", type="password", value="", icon=":material/password:"))

            st.space("small")
            col_new_account, col_go_to_log_in = st.columns(2, gap="small")
            if col_new_account.button("Create account", key="create_account_button", icon=":material/add_circle:", width="stretch"):
                if new_username and new_password:
                    if create_user_account(username=new_username, password=new_password):
                        st.session_state["new_user_data"] = None
                        if not st.session_state["new_user_data"]:   
                            from src.ui_components.dialogues import new_user_dialog
                            new_user_dialog()
                            st.stop()
                    else:
                        st.error("This username already exists, try another one.")
                else:
                    st.error("Invalid username or password")
            if st.session_state["new_user_data"] != False:
                user = initialize_new_user(user_id=new_username, name=st.session_state["new_user_data"]["name"], weight=st.session_state["new_user_data"]["weight"], height=st.session_state["new_user_data"]["height"])
                add_weigh_in(user=user, weight=st.session_state["new_user_data"]["weight"])
                st.session_state["new_user_data"] = False
                st.success("Your account was successfully created! Now, please log in.")

            col_go_to_log_in.button("Go to log in", key="go_to_log_in_button", icon=":material/login:", on_click=switch_tab, args=(":material/login: Log in",), width="stretch")

        if st.session_state["logged_in"] == False:
            st.stop()

def log_out():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.rerun()

def is_logged_in():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "user" not in st.session_state:
        st.session_state["user"] = None    
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] == False or st.session_state["user"] is None:
        st.session_state["logged_in"] = False
        log_in()

    st.sidebar.write(f"Logged in as: **@{st.session_state["user"].get_id()}**")
    if st.sidebar.button("Log out", width="stretch", icon=":material/logout:"):
        log_out()
    if st.session_state["user"].get_id() == "admin":
        st.sidebar.divider()
        st.sidebar.write("Admin tools:")
        if st.sidebar.button("Manage users", width="stretch", icon=":material/manage_accounts:"):
            from src.ui_components.dialogues import manage_users_dialog
            manage_users_dialog()

    return st.session_state["logged_in"]