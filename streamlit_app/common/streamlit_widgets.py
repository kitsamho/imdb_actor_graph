import streamlit as st
from typing import Tuple, List


def create_range_slider(label: str, min_value: float, max_value: float, default_range: Tuple[float, float], step: float) -> Tuple[float, float]:
    """
    Creates a range slider widget in Streamlit.

    Args:
        label: The label for the range slider.
        min_value: The minimum value of the range.
        max_value: The maximum value of the range.
        default_range: The default range as a tuple of (start, end) values.
        step: The step size of the range slider.

    Returns:
        The selected range as a tuple of (start, end) values.
    """
    range_values = st.sidebar.slider(label, min_value=min_value, max_value=max_value, value=default_range, step=step)
    return range_values


def st_expander(click: str, text: str) -> None:
    """
    Creates an expander widget in Streamlit.

    Args:
        click: The label for the expander widget.
        text: The content to be displayed inside the expander.
    """
    with st.expander(click):
        st.write(text)


