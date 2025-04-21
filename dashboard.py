import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

DATA_DIR = "data"

def admin_dashboard():
    st.title("📊 Admin Dashboard")
    st.markdown("Upload or browse session logs to analyze attention and drowsiness trends.")

    uploaded_file = st.file_uploader("Upload a session log (.csv)", type="csv")

    # Or select from stored logs
    available_logs = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    selected_log = st.selectbox("Or choose from saved sessions:", available_logs if available_logs else ["No logs found"])

    df = None
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    elif selected_log and selected_log != "No logs found":
        df = pd.read_csv(os.path.join(DATA_DIR, selected_log))

    if df is not None:
        st.success("Session data loaded successfully!")

        st.dataframe(df.tail(20))

        st.subheader("📈 EAR Over Time")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df["timestamp"], df["ear"], label="EAR", color="green")
        ax.axhline(y=0.21, color='r', linestyle='--', label='Drowsy Threshold')
        ax.set_xlabel("Time")
        ax.set_ylabel("EAR")
        ax.set_title("Eye Aspect Ratio Over Time")
        ax.legend()
        st.pyplot(fig)

        st.subheader("📊 Drowsiness Summary")
        below_threshold = df[df["ear"] < 0.21]
        drowsy_percent = len(below_threshold) / len(df) * 100
        st.metric(label="Drowsiness Events (%)", value=f"{drowsy_percent:.2f}%")
    else:
        st.info("Upload or select a log file to begin analysis.")
