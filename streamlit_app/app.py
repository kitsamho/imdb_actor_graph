import streamlit as st
from common.load import load_cached_file, load_config
from common.transform import _append_actor_url_to_df_actor_attributes
from common.transformers import DataLoader, MovieCastTransformer, D3Transformer, ActorGraphTransformer
from common.show import cache_d3_network_plot, plot_html, display_image_grid, plot_graph_metrics
from common.selection import mask_on_actor_edge_frequency, get_actor_co_star_dict, get_poster_paths, find_common_movies
from common.streamlit_widgets import st_expander

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# add logo
# st.sidebar.image('assets/tmdb_logo.png', width=200)

# create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Graph Visualisation", "Graph Metrics", "Common Movies", "About"])

# CONFIG
config_path = 'common/config.yaml'
config = load_config(config_path)
html_temp_file_path = config['DataPaths']['temp_html']
visualisation_info = config['PageInfo']
imdb_image_path = config['IMDBPaths']['Images']
about_page_info = config['AboutPage']

# LOAD DATA
loader = DataLoader(config_path=config_path)  # instantiate DataLoader object
loader.load_data()  # load and join the movies and cast data
df_merged = loader.get_df_merged()  # get the merged dataframe

# SELECT DATA
trf = MovieCastTransformer(df_merged)  # instantiate MovieCastTransformer object
df_merged_transformed = trf.transform_data()  # transform the merged dataframe

# TRANSFORM / FORMAT
d3_trf = D3Transformer(df_merged_transformed)
df_d3 = d3_trf.transform_data()

# GET GRAPH METRICS
graph_trf = ActorGraphTransformer(df_d3)
df_actor_graph_attributes = graph_trf.get_actor_graph_metrics_df()
graph_metrics_dict = graph_trf.get_actor_graph_metrics_dict()
edge_frequency_dict = graph_trf.get_edge_frequency_dict()

max_value = max(edge_frequency_dict.values())
min_value = min(edge_frequency_dict.values())

st.sidebar.markdown('---')
st.sidebar.subheader('Graph Filters')
min_threshold = st.sidebar.slider('Edge Frequency Threshold', min_value, max_value, 1)


with tab1:
    # VISUALISATION - NETWORK
    st.header('Graph Visualisation')
    st_expander('Click for info', visualisation_info['graph_plot'])
    df_d3_to_plot = mask_on_actor_edge_frequency(df_d3, edge_frequency_dict, min_threshold)
    cache_d3_network_plot(df_d3_to_plot, html_temp_file_path)
    cached_html = load_cached_file(html_temp_file_path)
    plot_html(cached_html)


with tab2:
    st.header('Graph Metrics')
    st_expander('Click for info', visualisation_info['graph_metrics'])
    df_actor_graph_attributes_url = _append_actor_url_to_df_actor_attributes(df_actor_graph_attributes, \
                                                                             df_merged_transformed, imdb_image_path)
    col1, col2 = st.columns(2)
    options_dict = {'Betweenness Centrality': 'BetweennessCentrality', 'Degree Centrality': 'DegreeCentrality',
                    'Eigenvector Centrality': 'EigenvectorCentrality', 'Clustering Coefficient': 'ClusteringCoefficient'}

    marker_size = st.slider('Adjust marker size', 1, 50, 5)
    x_axis = col1.selectbox("Select metric for x axis", options=sorted(list(options_dict.keys())))
    y_axis = col2.selectbox("Select metric for y axis", options=reversed(list(options_dict.keys())))

    plot = plot_graph_metrics(df_actor_graph_attributes_url,
                              options_dict[x_axis],
                              options_dict[y_axis],
                              size=marker_size)
    st.altair_chart(plot)

with tab3:
    st.header('Common Movies')
    actor_co_star_dict = get_actor_co_star_dict(df_d3_to_plot)
    col1, col2 = st.columns(2)
    selected_actor = col1.selectbox("Select an actor", options=sorted(list(actor_co_star_dict.keys())), key="actor_selectbox")
    selected_costar = col2.selectbox("Select an actor", options=sorted(actor_co_star_dict[selected_actor]), key="costar_selectbox")
    common_movies = find_common_movies(df_merged_transformed, selected_actor, selected_costar)
    paths = get_poster_paths(df_merged_transformed, common_movies, imdb_image_path)
    display_image_grid(paths)

with tab4:
    st.header('About')
    st.markdown(about_page_info['about'])
    st.subheader('Links')
    st.write(f'TMDB : {about_page_info["links"][0]}')
    st.write(f'd3Blocks : {about_page_info["links"][1]}')
    st.write(f'NetworkX : {about_page_info["links"][2]}')
    st.subheader('Contact')
    st.write(f'LinkedIn : {about_page_info["links"][3]}')
    st.write(f'Blog : {about_page_info["links"][4]}')

