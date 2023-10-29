import streamlit as st
import networkx as nx
import pandas as pd
import os

from .load import load_config
from .selection import select_gender, mask_range, select_movie_data, select_cast_data, get_min_max_values
from .transform import _get_nested_cast, _get_nested_cast_combinations, _flatten_nested_cast_combinations, \
    _get_combinations_dict, _get_d3_dataframe, join_movies_cast


class DataLoader:
    def __init__(self, config_path):
        """
        DataLoader class for loading movie and cast data.

        Args:
            config_path (str): Path to the YAML config file. Default is 'config.yaml'.
        """
        self.config_path = config_path
        self.data_path = None
        self.cast_data = None
        self.movies_data = None
        self.cast_path = None
        self.movies_path = None
        self.df_movies = None
        self.df_cast = None
        self.df_merged = None

    def load_data(self):
        """
        Load the movie and cast data from the specified file paths in the config file.
        """
        self.read_config()
        self.construct_file_paths()
        self.df_movies = self.read_data(self.movies_path)
        self.df_cast = self.read_data(self.cast_path)
        self.df_merged = self.join_movies_cast(self.df_cast, self.df_movies)

    def read_config(self):
        """
        Read the config file and extract the data paths.
        """
        config_data = load_config(self.config_path)
        data_paths = config_data['DataPaths']
        self.data_path = data_paths['data_path']
        self.cast_data = data_paths['cast_data']
        self.movies_data = data_paths['movies_data']

    def construct_file_paths(self):
        """
        Construct the full file paths using the extracted data paths.
        """
        try:
            self.cast_path = os.path.join(self.data_path, self.cast_data)
            self.movies_path = os.path.join(self.data_path, self.movies_data)
        except Exception as e:
            raise ValueError("Error constructing file paths: {}".format(str(e)))

    def read_data(self, file_path):
        """
        Read data from the specified file path.

        Args:
            file_path (str): Path to the data file.

        Returns:
            pandas.DataFrame: Loaded data as a DataFrame.
        """
        try:
            return pd.read_pickle(file_path)
        except Exception as e:
            raise ValueError("Error reading data from {}: {}".format(file_path, str(e)))

    def join_movies_cast(self, df_cast, df_movies):
        """
        Join the cast and movies dataframes on a common column.

        Args:
            df_cast (pandas.DataFrame): Cast dataframe.
            df_movies (pandas.DataFrame): Movies dataframe.

        Returns:
            pandas.DataFrame: Merged dataframe.
        """
        try:
            return join_movies_cast(df_cast, df_movies)
        except Exception as e:
            raise ValueError("Error joining cast and movies dataframes: {}".format(str(e)))

    def get_df_merged(self):
        """
        Get the merged dataframe.

        Returns:
            pandas.DataFrame: Merged dataframe.
        """
        return self.df_merged


class MovieCastTransformer:
    """
    A class for processing movie data based on user-selected filters.

    Args:
        merged_df (pandas.DataFrame): The merged dataframe containing movie and cast data.

    Attributes:
        merged_df (pandas.DataFrame): The merged dataframe containing movie and cast data.
        year_start (int): The start year selected by the user.
        year_end (int): The end year selected by the user.
        gender_choice (str): The gender choice selected by the user.

    """

    def __init__(self, merged_df):
        self.merged_df = merged_df
        self.year_start, self.year_end = self.__get_year_range()
        self.gender_choice = self.__select_gender()

    def __get_year_range(self):
        """
        Get the range of movie years selected by the user.

        Returns:
            Tuple[int, int]: The start and end year selected by the user.

        """
        st.sidebar.subheader('Movie Filters')
        min_year, max_year = get_min_max_values(self.merged_df, 'm_release_year', int)
        year_start, year_end = st.sidebar.slider('Year of release', min_year, max_year, (2021, 2023), 1)
        st.sidebar.text('caution - wide time frames are computationally intensive')

        return year_start, year_end

    def __select_gender(self):
        """
        Select the gender choice for filtering the cast data.

        Returns:
            str: The gender choice selected by the user.

        """
        return select_gender(st.sidebar.selectbox('Gender', ['Everyone', 'Male', 'Female']))

    def __filter_data(self):
        """
        Filter the movie and cast data based on user-selected filters.

        """
        # Filter movie data based on year and average rating
        self.merged_df = mask_range(self.merged_df, 'm_release_year', self.year_start, self.year_end)
        self.merged_df = select_movie_data(self.merged_df, self.year_start, self.year_end)

        # Filter cast data based on actor popularity and gender
        self.merged_df = select_cast_data(self.merged_df, self.gender_choice)

        # Perform any additional data processing or transformations

    def transform_data(self):
        """
        Process the movie data by filtering and transforming it based on user-selected filters.

        Returns:
            pandas.DataFrame: The processed dataframe containing the filtered movie and cast data.

        """
        # Filter and process data
        self.__filter_data()

        # Return processed data
        return self.merged_df


class D3Transformer:
    """
    Class to handle the transformation of processed data into a shape that can be used by the d3blocks network graph

    Parameters:
        df_transformed (pandas.DataFrame): The processed dataframe.

    """

    def __init__(self, df_transformed):
        self.df_transformed = df_transformed

    def __get_nested_cast(self):
        """
        Get the nested cast data.

        Returns:
            pandas.DataFrame: The dataframe with nested cast data.

        """
        df_nested = _get_nested_cast(self.df_transformed)
        return df_nested

    def __generate_nested_cast_combinations(self, df_nested):
        """
        Generate nested cast combinations.

        Parameters:
            df_nested (pandas.DataFrame): The dataframe with nested cast data.

        Returns:
            pandas.DataFrame: The dataframe with generated nested cast combinations.

        """
        df_nested['all_combinations'] = df_nested.c_name.apply(_get_nested_cast_combinations)
        return df_nested

    def __flatten_nested_cast_combinations(self, df_nested):
        """
        Flatten nested cast combinations.

        Parameters:
            df_nested (pandas.DataFrame): The dataframe with nested cast combinations.

        Returns:
            List[Tuple]: The flattened list of combination tuples.

        """
        flattened_combination_tuples = _flatten_nested_cast_combinations(df_nested)
        return flattened_combination_tuples

    def __get_combinations_dict(self, flattened_combination_tuples):
        """
        Generate combinations dictionary.

        Parameters:
            flattened_combination_tuples (List[Tuple]): The flattened list of combination tuples.

        Returns:
            Dict: The combinations dictionary.

        """
        combinations_dict = _get_combinations_dict(flattened_combination_tuples)
        return combinations_dict

    def __get_d3_dataframe(self, combinations_dict):
        """
        Get the D3 dataframe.

        Parameters:
            combinations_dict (Dict): The combinations dictionary.

        Returns:
            pandas.DataFrame: The D3 dataframe.

        """
        df_d3 = _get_d3_dataframe(combinations_dict)
        return df_d3

    def transform_data(self):
        """
        Perform the data transformation.

        Returns:
            pandas.DataFrame: The transformed D3 dataframe.

        """
        df_nested = self.__get_nested_cast()
        df_nested = self.__generate_nested_cast_combinations(df_nested)
        flattened_combination_tuples = self.__flatten_nested_cast_combinations(df_nested)
        combinations_dict = self.__get_combinations_dict(flattened_combination_tuples)
        df_d3 = self.__get_d3_dataframe(combinations_dict)
        return df_d3


class ActorGraphTransformer:
    """
    A class for transforming a DataFrame into an actor graph and calculating various graph metrics.

    Attributes:
        df_d3 (pandas.DataFrame): The input DataFrame containing the graph data.
        graph (networkx.Graph): The graph representation of the DataFrame.
        actor_graph_metrics_df (pandas.DataFrame): DataFrame containing the calculated graph metrics for each actor.
        actor_graph_metrics_dict (dict): Dictionary containing the graph metrics for each actor.
        edge_frequency_dict (dict): Dictionary containing the frequency of edges in the graph.

    Methods:
        __create_graph(): Create a graph from the DataFrame.
        __create_graph_df(): Calculate various graph metrics for each actor and return a DataFrame.
        __create_actor_metrics_dict(): Create a dictionary of graph metrics for each actor.
        __get_edge_frequency_dict(): Calculate the frequency of edges in the graph.
        get_actor_graph_metrics_df(): Get the DataFrame containing graph metrics for each actor.
        get_actor_graph_metrics_dict(): Get the dictionary of graph metrics for each actor.
        get_edge_frequency_dict(): Get the dictionary containing the frequency of edges in the graph.
    """

    def __init__(self, df_d3):
        """
        Initialize the ActorGraphTransformer class.

        Args:
            df_d3 (pandas.DataFrame): The input DataFrame containing the graph data.
        """
        self.df_d3 = df_d3
        self.graph = self.__create_graph()
        self.actor_graph_metrics_df = self.__create_graph_df()
        self.actor_graph_metrics_dict = self.__create_actor_metrics_dict()
        self.edge_frequency_dict = self.__get_edge_frequency_dict()

    def __create_graph(self):
        """
        Create a graph from the DataFrame.

        Returns:
            networkx.Graph: The graph representation of the DataFrame.

        Raises:
            ValueError: If an error occurs while creating the graph.
        """
        try:
            graph = nx.from_pandas_edgelist(self.df_d3, 'source', 'target', 'weight')
            return graph
        except Exception as e:
            raise ValueError("Error creating the graph: " + str(e))

    def __create_graph_df(self):
        """
        Calculate various graph metrics for each actor and return a DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing the calculated graph metrics for each actor.

        Raises:
            ValueError: If an error occurs while creating the actor attributes DataFrame.
        """
        try:
            actor_attributes = pd.DataFrame(index=self.graph.nodes)

            actor_attributes['DegreeCentrality'] = pd.Series(nx.degree_centrality(self.graph))
            actor_attributes['BetweennessCentrality'] = pd.Series(nx.betweenness_centrality(self.graph))
            actor_attributes['EigenvectorCentrality'] = pd.Series(nx.eigenvector_centrality(self.graph))
            actor_attributes['ClusteringCoefficient'] = pd.Series(nx.clustering(self.graph))

            return round(actor_attributes, 3).reset_index().rename(columns={'index': 'Actor'})
        except Exception as e:
            raise ValueError("Error creating actor attributes: " + str(e))

    def __create_actor_metrics_dict(self):
        """
        Create a dictionary of graph metrics for each actor.

        Returns:
            dict: Dictionary containing the graph metrics for each actor.

        Raises:
            ValueError: If an error occurs while creating the actor metrics dictionary.
        """
        try:
            actor_dict = {}
            for actor, attributes in self.actor_graph_metrics_df.iterrows():
                actor_dict[str(actor).replace(" ", "_")] = attributes.to_dict()
            return actor_dict
        except Exception as e:
            raise ValueError("Error creating actor metrics dictionary: " + str(e))

    def __get_edge_frequency_dict(self):
        """
        Calculate the frequency of edges in the graph.

        Returns:
            dict: Dictionary containing the frequency of edges in the graph.

        Raises:
            ValueError: If an error occurs while getting the edge frequency dictionary.
        """
        try:
            source_counts = self.df_d3['source'].value_counts().to_dict()
            target_counts = self.df_d3['target'].value_counts().to_dict()
            result = {key: source_counts.get(key, 0) + target_counts.get(key, 0) for key in source_counts}
            return result
        except Exception as e:
            raise ValueError("Error getting edge frequency dictionary: " + str(e))

    def get_actor_graph_metrics_df(self):
        """
        Get the DataFrame containing graph metrics for each actor.

        Returns:
            pandas.DataFrame: DataFrame containing graph metrics for each actor.
        """
        return self.actor_graph_metrics_df

    def get_actor_graph_metrics_dict(self):
        """
        Get the dictionary of graph metrics for each actor.

        Returns:
            dict: Dictionary containing graph metrics for each actor.
        """
        return self.actor_graph_metrics_dict

    def get_edge_frequency_dict(self):
        """
        Get the dictionary containing the frequency of edges in the graph.

        Returns:
            dict: Dictionary containing the frequency of edges in the graph.
        """
        return self.edge_frequency_dict


