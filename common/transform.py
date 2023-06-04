import itertools
import pandas as pd


def join_movies_cast(df_masked_cast, df_masked_movies):
    df_cast_movies = pd.merge(df_masked_cast, df_masked_movies, how='inner', left_on='c_tmdb_id',
                              right_on='m_tmdb_id')
    return df_cast_movies


def _get_nested_cast(df_cast_movies):
    df_nested = pd.DataFrame(df_cast_movies.groupby('m_movie')['c_name'].agg(lambda x: list(x)))
    solo_cast_mask = df_nested.c_name.apply(lambda x: len(x)>=2)
    df_nested = df_nested[solo_cast_mask]
    return df_nested


def _get_nested_cast_combinations(cast):
    if len(cast) > 1:
        actor_combinations = itertools.combinations(cast, 2)
        actor_combinations_sorted = [tuple(sorted(combination)) for combination in actor_combinations]
        return actor_combinations_sorted
    else:
        return cast

def _flatten_nested_cast_combinations(df_nested):
    flattened_combination_tuples = []
    for combinations_in_film in df_nested.all_combinations.values:
        for combination in combinations_in_film:
            flattened_combination_tuples.append(combination)
    return flattened_combination_tuples


def _get_combinations_dict(flattened_combination_tuples):
    combinations_dict = {}
    for flattened_combination_tuple in flattened_combination_tuples:
        if flattened_combination_tuple in combinations_dict:
            combinations_dict[flattened_combination_tuple] += 1
        else:
            combinations_dict[flattened_combination_tuple] = 1
    return combinations_dict


def _get_d3_dataframe(combinations_dict):
    df_d3 = pd.DataFrame(combinations_dict.items())
    df_d3 = pd.concat([df_d3[0].apply(pd.Series), df_d3[1]], axis=1)
    df_d3.columns = ['source', 'target', 'weight']
    return df_d3


def _append_actor_url_to_df_actor_attributes(df_actor_attributes, df_cast_movies, imdb_image_path):
    df_actor_attributes = df_actor_attributes.merge(df_cast_movies[['c_name', 'c_profile_path']].drop_duplicates \
                                                        (subset='c_name', keep='first'), left_on='Actor',
                                                    right_on='c_name').drop(columns='c_name')
    df_actor_attributes['c_profile_path'] = df_actor_attributes['c_profile_path'].apply(lambda x: imdb_image_path+x)
    return df_actor_attributes.rename(columns={'c_profile_path': 'image'})




