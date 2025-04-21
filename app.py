import streamlit as st
from login import login_page
from detection import detection_page
from dashboard import admin_dashboard

# Set wide layout 
st.set_page_config(page_title="Drowsiness & Gaze Tracker", layout="wide")

# Simple user session (demo purpose)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None

st.sidebar.title("Navigation")

if not st.session_state.logged_in:
    login_page()

else:
    if st.session_state.user_type == "user":
        page = st.sidebar.radio("Go to", ["Detection"])
        if page == "Detection":
            detection_page()

    elif st.session_state.user_type == "admin":
        page = st.sidebar.radio("Go to", ["Dashboard"])
        if page == "Dashboard":
            admin_dashboard()

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.rerun()
