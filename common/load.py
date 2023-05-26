import pandas as pd
import streamlit as st

@st.cache_data
def read_data(path):
    return pd.read_pickle(path)


def _load_cached_file(save_path):
    with open(save_path, "r") as f:
        file = f.read()
    return file