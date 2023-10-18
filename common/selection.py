import pandas as pd
from collections import defaultdict
from typing import List, Union, Optional


def mask_range(df: pd.DataFrame, col: str, start: Union[int, float], end: Union[int, float]) -> pd.DataFrame:
    """
    Filter rows of a DataFrame based on a range of values in a specific column.

    Args:
        df: The DataFrame to filter.
        col: The name of the column to filter on.
        start: The lower bound of the range.
        end: The upper bound of the range.

    Returns:
        The filtered DataFrame.
    """
    return df[(df[col] >= start) & (df[col] <= end)]


def mask_value(df: pd.DataFrame, col: str, value: Union[int, float]) -> pd.DataFrame:
    """
    Filter rows of a DataFrame based on a specific value in a specific column.

    Args:
        df: The DataFrame to filter.
        col: The name of the column to filter on.
        value: The value to filter for.

    Returns:
        The filtered DataFrame.
    """
    return df[df[col] == value]


def get_min_max_values(df: pd.DataFrame, col: str, number_type: type) -> tuple:
    """
    Get the minimum and maximum values from a specific column of a DataFrame.

    Args:
        df: The DataFrame to analyze.
        col: The name of the column.
        number_type: The type of the column (e.g., int, float).

    Returns:
        A tuple containing the minimum and maximum values.
    """
    min_value, max_value = number_type(df[col].min()), number_type(df[col].max())
    return min_value, max_value


def select_movie_data(df_movies: pd.DataFrame, year_start: Optional[int] = None,
                      year_end: Optional[int] = None) -> pd.DataFrame:
    """
    Select movie data from a DataFrame based on specified criteria.

    Args:
        df_movies: The DataFrame containing movie data.
        year_start: The start year of the movies.
        year_end: The end year of the movies.

    Returns:
        The filtered DataFrame.
    """
    if year_start:
        df_movies = mask_range(df_movies, 'm_release_year', year_start, year_end)
    return df_movies


def select_gender(gender_choice: str) -> Union[float, None]:
    """
    Select the gender value based on the provided choice.

    Args:
        gender_choice: The selected gender choice.

    Returns:
        The gender value (1.0 for female, 2.0 for male) or None if "Everyone" is chosen.
    """
    if gender_choice == 'Everyone':
        gender_mask = None
    elif gender_choice == 'Male':
        gender_mask = 2.0
    elif gender_choice == 'Female':
        gender_mask = 1.0
    return gender_mask


def select_cast_data(df_cast: pd.DataFrame, gender: Optional[float] = None) -> pd.DataFrame:
    """
    Select cast data from a DataFrame based on specified criteria.

    Args:
        df_cast: The DataFrame containing cast data.
        gender: The selected gender.

    Returns:
        The filtered DataFrame.
    """
    if gender:
        df_cast = mask_value(df_cast, 'c_gender', gender)
    return df_cast


def mask_on_actor_edge_frequency(df_d3: pd.DataFrame, edge_frequency_dict: dict, min_threshold: int) -> pd.DataFrame:
    """
    Filter edges in a DataFrame based on the frequency of the actors in the edge.

    Args:
        df_d3: The DataFrame containing edge data.
        edge_frequency_dict: A dictionary containing actor frequencies.
        min_threshold: The minimum threshold for actor frequency.

    Returns:
        The filtered DataFrame.
    """
    actors_to_mask = [k for k, v in edge_frequency_dict.items() if v > min_threshold]
    mask = df_d3['source'].isin(actors_to_mask) & df_d3['target'].isin(actors_to_mask)
    return df_d3[mask].reset_index(drop=True)


def get_actor_co_star_dict(df_d3_masked: pd.DataFrame) -> dict:
    """
    Get a dictionary of actors and their co-stars from a DataFrame of masked edges.

    Args:
        df_d3_masked: The DataFrame containing masked edge data.

    Returns:
        A dictionary mapping actors to their co-stars.
    """
    dic_merged = defaultdict(list)

    for source, target in zip(df_d3_masked['source'], df_d3_masked['target']):
        dic_merged[source].append(target)
        dic_merged[target].append(source)

    dic_source_target = dict(dic_merged)
    return dic_source_target


def find_common_movies(df: pd.DataFrame, actor1: str, actor2: str) -> List[str]:
    """
    Find common movies between two actors in a DataFrame.

    Args:
        df: The DataFrame containing actor and movie data.
        actor1: The name of the first actor.
        actor2: The name of the second actor.

    Returns:
        A list of common movie names.
    """
    actor1_movies = set(df[df['c_name'] == actor1]['m_movie'])
    actor2_movies = set(df[df['c_name'] == actor2]['m_movie'])
    common_movies = actor1_movies.intersection(actor2_movies)
    return list(common_movies)


def get_poster_paths(df: pd.DataFrame, common_movies: List[str], imdb_image_path: str) -> List[tuple]:
    """
    Get the poster paths for common movies from a DataFrame.

    Args:
        df: The DataFrame containing movie data.
        common_movies: A list of common movie names.
        imdb_image_path: The base URL for the movie poster images.

    Returns:
        A list of tuples containing the movie name and its corresponding poster path.
    """
    res = []
    for movie in common_movies:
        poster_path = df[df['m_movie'] == movie]['m_poster_path'].unique()[0]
        res.append((movie, imdb_image_path + poster_path))
    return res
