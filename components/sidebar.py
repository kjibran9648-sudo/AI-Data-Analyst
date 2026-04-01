import streamlit as st

def sidebar_options():
    st.sidebar.title("⚙️ Options")
    return st.sidebar.radio("Select Action", [
        "Overview",
        "Data Cleaning",
        "Insights",
        "Profiling"
    ])