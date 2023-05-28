import os

import streamlit as st

from common.graph import ActorGraphMetrics, create_actor_graph_metrics_dict
from common.load import read_data, _load_cached_file
from common.show import _cache_d3_network_plot, plot_html, display_image_grid
from common.streamlit_widgets import create_range_slider
from common.select import _select_movie_data, _select_cast_data, _mask_on_actor_edge_frequency, _mask_range, \
    _get_actor_co_star_dict, _get_poster_paths, _find_common_movies, _mask_value, _select_gender, _get_min_max_values
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

df_merged = join_movies_cast(df_cast, df_movies)


#### Movies Section
st.sidebar.header('Movie Filters')

# filter on movie year
min_year, max_year = _get_min_max_values(df_merged, 'm_release_year', int)
year_start, year_end = st.sidebar.slider('Year of release', min_year, max_year, (2018, 2023), 1)
df_merged = _mask_range(df_merged, 'm_release_year', year_start, year_end)

min_vote, max_vote = _get_min_max_values(df_merged, 'm_vote_average', float)
vote_start, vote_end = st.sidebar.slider('Average movie rating', min_vote, max_vote, \
                               (6.0, max_vote), 0.1)

df_merged = _select_movie_data(df_merged,
                              year_start, year_end,
                              vote_start, vote_end)



st.sidebar.markdown("----")

st.sidebar.header('Actor Filters')


min_actor_popularity, max_actor_popularity = _get_min_max_values(df_merged, 'c_popularity', float)


actor_popularity_start, actor_popularity_end = st.sidebar.slider('Popularity', min_actor_popularity, max_actor_popularity, \
                                           (min_actor_popularity, max_actor_popularity), 1.0)


gender_choice = _select_gender(st.sidebar.radio('Gender', ['Everyone', 'Male', 'Female']))

# Filter cast data
df_transformed = _select_cast_data(df_merged, actor_popularity_start, actor_popularity_end, gender_choice)

# Join movie and cast data


# Get nested cast data
df_nested = _get_nested_cast(df_transformed)

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

common_movies = _find_common_movies(df_transformed, selected_actor, selected_costar)

paths = _get_poster_paths(df_transformed, common_movies)

display_image_grid(paths)