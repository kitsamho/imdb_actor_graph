import streamlit as st
import altair as alt
from d3blocks import D3Blocks

def cache_d3_network_plot(df_d3_masked,
                           file_path,
                           edge_distance=100,
                           node_size=4,
                           fontsize=8):

    d3 = D3Blocks()
    d3.d3graph(df_d3_masked)
    d3.D3graph.set_edge_properties(directed=False, edge_distance=edge_distance)
    d3.D3graph.set_node_properties(color='cluster', size=node_size, edge_size=0.2, fontsize=fontsize)
    d3.D3graph.show(filepath=file_path)
    return


def plot_html(cached_html, image_size=(950, 550)):
    st.components.v1.html(cached_html, width=image_size[0], height=image_size[1])
    return


def display_image_grid(paths):
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


def plot_graph_metrics(df, x_axis, y_axis, size=40, height=800, width=800):
    """
    Plots a scatter plot to visualize the graph metrics.

    Args:
        df (pandas.DataFrame): DataFrame containing the graph metrics.
        x_axis (str): Name of the column representing the x-axis.
        y_axis (str): Name of the column representing the y-axis.
        size (int, optional): Size of the markers in the scatter plot. Default is 40.
        height (int, optional): Height of the plot in pixels. Default is 800.
        width (int, optional): Width of the plot in pixels. Default is 800.

    Returns:
        altair.Chart: The scatter plot visualization.
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




