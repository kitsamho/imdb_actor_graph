import streamlit as st

from d3blocks import D3Blocks


def _cache_d3_network_plot(df_d3_masked,
                           file_path,
                           edge_distance=100,
                           node_size=4,
                           fontsize=8):

    d3 = D3Blocks()
    d3.d3graph(df_d3_masked, title='dsfsdf')
    d3.D3graph.set_edge_properties(directed=False, edge_distance=edge_distance)
    d3.D3graph.set_node_properties(color='cluster', size=node_size, edge_size=0.2, fontsize=fontsize)
    d3.D3graph.show(filepath=file_path)
    return


def plot_html(cached_html, image_size=(950,950)):
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



