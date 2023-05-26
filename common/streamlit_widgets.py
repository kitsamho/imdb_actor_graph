import streamlit as st

def create_range_slider(label, min_value, max_value, default_range, step):
    range_values = st.sidebar.slider(label, min_value=min_value, max_value=max_value, value=default_range, step=step)
    return range_values