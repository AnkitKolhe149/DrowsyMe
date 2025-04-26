# import streamlit as st

# def login_page():
#     st.title("🔐 Login to Start Monitoring")

#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         user_type = st.radio("Login as", ["user", "admin"])
#         submitted = st.form_submit_button("Login")

#         if submitted:
#             # Dummy authentication (replace with real DB/auth logic)
#             if user_type == "user" and username == "user" and password == "1234":
#                 st.success("Welcome, user!")
#                 st.session_state.logged_in = True
#                 st.session_state.user_type = "user"
#                 st.rerun()

#             elif user_type == "admin" and username == "admin" and password == "admin123":
#                 st.success("Welcome, admin!")
#                 st.session_state.logged_in = True
#                 st.session_state.user_type = "admin"
#                 st.rerun()

#             else:
#                 st.error("Invalid credentials. Try again.")


# login.py

import streamlit as st
from utils.auth import register_user, authenticate_user

def login_page():
    st.title("🔐 Welcome to DrowsyMe Monitoring")

    option = st.radio("Select option", ["Login", "Register"])

    if option == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            user_type = st.radio("Login as", ["user", "admin"])
            submitted = st.form_submit_button("Login")

            if user_type == "admin" and username == "admin" and password == "admin123":
                 st.success("Welcome, admin!")
                 st.session_state.logged_in = True
                 st.session_state.user_type = "admin"
                 st.rerun()

            if submitted:
                is_authenticated = authenticate_user(username, password, user_type)
                if is_authenticated:
                    st.success(f"Welcome, {username}!")
                    st.session_state.logged_in = True
                    st.session_state.user_type = user_type
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

    elif option == "Register":
        with st.form("register_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_user_type = st.radio("Register as", ["user"])  # Only users allowed to register
            submitted = st.form_submit_button("Register")

            if submitted:
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(new_username, new_password, new_user_type)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
