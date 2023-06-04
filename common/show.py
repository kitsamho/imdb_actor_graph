import pandas as pd
import streamlit as st
import altair as alt
from d3blocks import D3Blocks
from typing import List, Tuple


def cache_d3_network_plot(df_d3_masked: pd.DataFrame, file_path: str, edge_distance: int = 100,
                          node_size: int = 4, fontsize: int = 8) -> None:
    """
    Caches a D3 network plot to a file.

    Args:
        df_d3_masked: The DataFrame containing masked edge data.
        file_path: The path to save the cached plot file.
        edge_distance: The distance between nodes in the plot.
        node_size: The size of the nodes in the plot.
        fontsize: The font size of the nodes in the plot.
    """
    d3 = D3Blocks()
    d3.d3graph(df_d3_masked)
    d3.D3graph.set_edge_properties(directed=False, edge_distance=edge_distance)
    d3.D3graph.set_node_properties(color='cluster', size=node_size, edge_size=0.2, fontsize=fontsize)
    d3.D3graph.show(filepath=file_path)


def plot_html(cached_html: str, image_size: Tuple[int, int] = (950, 550)) -> None:
    """
    Displays a cached HTML plot in Streamlit.

    Args:
        cached_html: The path to the cached HTML plot file.
        image_size: The size of the displayed image in Streamlit.
    """
    st.components.v1.html(cached_html, width=image_size[0], height=image_size[1])


def display_image_grid(paths: List[Tuple[str, str]]) -> None:
    """
    Displays a grid of images in Streamlit.

    Args:
        paths: A list of tuples containing the image caption and path.
    """
    num_images = len(paths)

    # Calculate the grid size based on the number of images
    if num_images <= 4:
        grid_cols = num_images
        grid_rows = 1
    else:
        grid_cols = 4
        grid_rows = (num_images + grid_cols - 1) // grid_cols

    # Create the image grid
    for i in range(grid_rows):
        cols = st.columns(grid_cols)
        for j in range(grid_cols):
            idx = i * grid_cols + j
            if idx < num_images:
                cols[j].image(paths[idx][1], caption=paths[idx][0], use_column_width=True)
            else:
                break


def plot_graph_metrics(df: pd.DataFrame, x_axis: str, y_axis: str, size: int = 40,
                       height: int = 800, width: int = 800) -> alt.Chart:
    """
    Plots a scatter plot to visualize the graph metrics.

    Args:
        df: DataFrame containing the graph metrics.
        x_axis: Name of the column representing the x-axis.
        y_axis: Name of the column representing the y-axis.
        size: Size of the markers in the scatter plot. Default is 40.
        height: Height of the plot in pixels. Default is 800.
        width: Width of the plot in pixels. Default is 800.

    Returns:
        The scatter plot visualization as an altair.Chart object.
    """
    marker_chart = alt.Chart(df).mark_circle(size=size).encode(
        x=x_axis,
        y=y_axis,
        tooltip=['image', 'Actor']  # Must be a list containing a field called "image"
    ).properties(
        width=height,
        height=width
    )

    return marker_chart
