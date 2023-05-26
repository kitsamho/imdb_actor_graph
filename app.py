import os

import streamlit as st

from common.graph import ActorGraphMetrics, create_actor_graph_metrics_dict
from common.load import read_data, _load_cached_file
from common.show import _cache_d3_network_plot, plot_html, display_image_grid
from common.streamlit_widgets import create_range_slider
from common.select import _select_movie_data, _select_cast_data, _mask_on_actor_edge_frequency, _mask_range, \
    _get_actor_co_star_dict, _get_poster_paths, _find_common_movies, _mask_value, _select_gender
from common.transform import join_movies_cast, _get_nested_cast, _get_nested_cast_combinations, \
    _flatten_nested_cast_combinations, _get_combinations_dict, _get_d3_dataframe, _get_edge_frequency_dict

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Define file paths
data_path = 'cached_data'
cast_data = 'cast.pickle'
movies_data = 'movies.pickle'
file_path = '_temp_html/d3_graph.html'

# Construct full file paths
cast_path = os.path.join(data_path, cast_data)
movies_path = os.path.join(data_path, movies_data)

# Read data
df_movies = read_data(movies_path)
df_cast = read_data(cast_path)


#### Movies Section
st.sidebar.header('Movie Filters')

# filter on movie year
year_range = st.sidebar.slider('Year of release', 1990, 2023, (2018, 2023), 1)
year_start, year_end = year_range

df_movies = _mask_range(df_movies, 'm_release_year', year_range[0], year_range[1])

vote_low_slider, vote_high_slider = float(df_movies.m_vote_average.min()), float(df_movies.m_vote_average.max())

vote_range = st.sidebar.slider('Average movie rating', vote_low_slider, vote_high_slider, \
                               (6.0, vote_high_slider), 0.1)
vote_low, vote_high = vote_range


# Filter movie data
df_masked_movies = _select_movie_data(df_movies,
                                      year_start, year_end,
                                      vote_low, vote_high)

st.sidebar.markdown("----")
# Actor filters
st.sidebar.header('Actor Filters')

actor_popularity_low, actor_popularity_high = 1.0, 100.0
actor_popularity_range = st.sidebar.slider('Actor popularity', actor_popularity_low, actor_popularity_high, (25.0, 100.0), 1.0)
actor_popularity_low, actor_popularity_high = actor_popularity_range

gender_choice = _select_gender(st.sidebar.radio('Gender', ['Everyone', 'Male', 'Female']))

# Filter cast data
df_masked_cast = _select_cast_data(df_cast, actor_popularity_low, actor_popularity_high, gender_choice)

# Join movie and cast data
df_cast_movies = join_movies_cast(df_masked_cast, df_masked_movies)

# Get nested cast data
df_nested = _get_nested_cast(df_cast_movies)

# Generate nested cast combinations
df_nested['all_combinations'] = df_nested.c_name.apply(_get_nested_cast_combinations)

# Flatten nested cast combinations
flattened_combination_tuples = _flatten_nested_cast_combinations(df_nested)


# Generate combinations dictionary
combinations_dict = _get_combinations_dict(flattened_combination_tuples)

# Get D3 dataframe
df_d3 = _get_d3_dataframe(combinations_dict)

# get graph metrics from d3 dataframe using ActorGraphMetrics object
actor_graph_metrics = ActorGraphMetrics(df_d3)
df_actor_attributes = actor_graph_metrics.get_actor_attributes()

# compute graph metrics dictionary
actor_graph_metrics_dict = create_actor_graph_metrics_dict(df_actor_attributes)

# Compute edge frequency dictionary
edge_frequency_dict = _get_edge_frequency_dict(df_d3)



max_value = max(edge_frequency_dict.values())
min_value = min(edge_frequency_dict.values())



min_threshold = st.sidebar.slider('Edge Frequency Threshold',min_value, max_value,1)
st.write(min_threshold)
# Mask on actor edge frequency
df_d3_to_plot = _mask_on_actor_edge_frequency(df_d3, edge_frequency_dict, min_threshold)

# Cache D3 network plot
_cache_d3_network_plot(df_d3_to_plot, file_path)

# Load cached HTML file
cached_html = _load_cached_file(file_path)

st.header('Graph Visualisation')
# Plot HTML
plot_html(cached_html)

st.markdown("----")
st.header('Films Starred In')

actor_co_star_dict = _get_actor_co_star_dict(df_d3_to_plot)

col1, col2 = st.columns(2)

# Display select box for keys in the first column
selected_actor = col1.selectbox("Select a key", options=list(actor_co_star_dict.keys()))

# Display select box for values in the second column
selected_costar = col2.selectbox("Select a value", options=actor_co_star_dict[selected_actor])

common_movies = _find_common_movies(df_cast_movies,selected_actor, selected_costar)

paths = _get_poster_paths(df_cast_movies, common_movies)

display_image_grid(paths)