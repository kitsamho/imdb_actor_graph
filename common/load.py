import pandas as pd
import streamlit as st
import yaml
from typing import Dict


@st.cache_data
def read_data(path: str) -> pd.DataFrame:
    """
    Read data from a file using Pandas' read_pickle function.

    Args:
        path: Path to the file.

    Returns:
        The loaded DataFrame.
    """
    return pd.read_pickle(path)


def load_cached_file(save_path: str) -> str:
    """
    Load a file from a specified path.

    Args:
        save_path: Path to the file.

    Returns:
        The content of the file as a string.
    """
    with open(save_path, "r") as f:
        file = f.read()
    return file


# def load_config(path: str) -> Dict:
#     """
#     Load a YAML configuration file.
#
#     Args:
#         path: Path to the YAML configuration file.
#
#     Returns:
#         The loaded configuration data as a dictionary.
#     """
#     with open(path, 'r') as f:
#         config_data = yaml.safe_load(f)
#     return config_data

@st.cache_data
def load_config(path: str) -> Dict:

    with open(path, 'r') as config_file:
        yml_file = yaml.load(config_file, Loader=yaml.FullLoader)
    return yml_file
