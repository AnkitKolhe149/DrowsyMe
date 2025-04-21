import streamlit as st

def login_page():
    st.title("🔐 Login to Start Monitoring")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.radio("Login as", ["user", "admin"])
        submitted = st.form_submit_button("Login")

        if submitted:
            # Dummy authentication (replace with real DB/auth logic)
            if user_type == "user" and username == "user" and password == "1234":
                st.success("Welcome, user!")
                st.session_state.logged_in = True
                st.session_state.user_type = "user"
                st.rerun()

            elif user_type == "admin" and username == "admin" and password == "admin123":
                st.success("Welcome, admin!")
                st.session_state.logged_in = True
                st.session_state.user_type = "admin"
                st.rerun()

            else:
                st.error("Invalid credentials. Try again.")
