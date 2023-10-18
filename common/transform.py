import itertools
import pandas as pd
from typing import List, Dict


def join_movies_cast(df_masked_cast: pd.DataFrame, df_masked_movies: pd.DataFrame) -> pd.DataFrame:
    """
    Joins the masked cast DataFrame with the masked movies DataFrame.

    Args:
        df_masked_cast: The masked cast DataFrame.
        df_masked_movies: The masked movies DataFrame.

    Returns:
        The joined DataFrame.
    """
    df_cast_movies = pd.merge(df_masked_cast, df_masked_movies, how='inner', left_on='c_tmdb_id',
                              right_on='m_tmdb_id')
    return df_cast_movies


def _get_nested_cast(df_cast_movies: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the nested cast DataFrame from the joined DataFrame.

    Args:
        df_cast_movies: The joined DataFrame.

    Returns:
        The nested cast DataFrame.
    """
    df_nested = pd.DataFrame(df_cast_movies.groupby('m_movie')['c_name'].agg(lambda x: list(x)))
    solo_cast_mask = df_nested.c_name.apply(lambda x: len(x) >= 2)
    df_nested = df_nested[solo_cast_mask]
    return df_nested


def _get_nested_cast_combinations(cast: List[str]) -> List[tuple]:
    """
    Generates all combinations of actors from the given cast.

    Args:
        cast: The list of actors.

    Returns:
        The list of combinations of actors.
    """
    if len(cast) > 1:
        actor_combinations = itertools.combinations(cast, 2)
        actor_combinations_sorted = [tuple(sorted(combination)) for combination in actor_combinations]
        return actor_combinations_sorted
    else:
        return cast


def _flatten_nested_cast_combinations(df_nested: pd.DataFrame) -> List[tuple]:
    """
    Flattens the nested cast combinations into a flat list of tuples.

    Args:
        df_nested: The nested cast DataFrame.

    Returns:
        The flattened list of tuples.
    """
    flattened_combination_tuples = []
    for combinations_in_film in df_nested.all_combinations.values:
        for combination in combinations_in_film:
            flattened_combination_tuples.append(combination)
    return flattened_combination_tuples


def _get_combinations_dict(flattened_combination_tuples: List[tuple]) -> Dict[tuple, int]:
    """
    Counts the occurrences of each combination in the flattened list and creates a dictionary.

    Args:
        flattened_combination_tuples: The flattened list of tuples.

    Returns:
        The dictionary with combinations as keys and their occurrence count as values.
    """
    combinations_dict = {}
    for flattened_combination_tuple in flattened_combination_tuples:
        if flattened_combination_tuple in combinations_dict:
            combinations_dict[flattened_combination_tuple] += 1
        else:
            combinations_dict[flattened_combination_tuple] = 1
    return combinations_dict


def _get_d3_dataframe(combinations_dict: Dict[tuple, int]) -> pd.DataFrame:
    """
    Converts the combinations dictionary into a DataFrame compatible with D3 visualization.

    Args:
        combinations_dict: The dictionary with combinations and their occurrence count.

    Returns:
        The DataFrame compatible with D3 visualization.
    """
    df_d3 = pd.DataFrame(combinations_dict.items())
    df_d3 = pd.concat([df_d3[0].apply(pd.Series), df_d3[1]], axis=1)
    df_d3.columns = ['source', 'target', 'weight']
    return df_d3


def _append_actor_url_to_df_actor_attributes(df_actor_attributes: pd.DataFrame, df_cast_movies: pd.DataFrame,\
                                             imdb_image_path: str) -> pd.DataFrame:
    """
    Appends the URL of actor images to the actor attributes DataFrame.

    Args:
        df_actor_attributes: The actor attributes DataFrame.
        df_cast_movies: The joined DataFrame.
        imdb_image_path: The path to the IMDb image directory.

    Returns:
        The updated actor attributes DataFrame.
    """
    df_actor_attributes = df_actor_attributes.merge(df_cast_movies[['c_name', 'c_profile_path']].drop_duplicates \
                                                        (subset='c_name', keep='first'), left_on='Actor',
                                                    right_on='c_name').drop(columns='c_name')
    df_actor_attributes['c_profile_path'] = df_actor_attributes['c_profile_path'].apply(lambda x: imdb_image_path + x)
    return df_actor_attributes.rename(columns={'c_profile_path': 'image'})

