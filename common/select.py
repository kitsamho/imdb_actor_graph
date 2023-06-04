from collections import defaultdict


def mask_range(df, col, start, end):
    return df[(df[col] >= start) & (df[col] <= end)]


def mask_value(df, col, value):
    return df[df[col] == value]


def get_min_max_values(df, col, number_type):
    min_value, max_value = number_type(df[col].min()), number_type(df[col].max())
    return min_value, max_value


def select_movie_data(df_movies,year_start, year_end=None,
                       # revenue_low=None, revenue_high=None,
                       # budget_low=None, budget_high=None,
                       vote_low=None, vote_high=None):


    if year_start:
        df_movies = mask_range(df_movies, 'm_release_year', year_start, year_end)
    if vote_low:
        df_movies = mask_range(df_movies, 'm_vote_average', vote_low, vote_high)

    return df_movies


def select_gender(gender_choice):
    if gender_choice == 'Everyone':
        gender_mask = None
    elif gender_choice == 'Male':
        gender_mask = 2.0
    elif gender_choice == 'Female':
        gender_mask = 1.0
    return gender_mask


def select_cast_data(df_cast,
                      popularity_low=None, popularity_high=None,
                      gender=None,
                      adult=None):

    if popularity_low:
        df_cast = mask_range(df_cast, 'c_popularity', popularity_low, popularity_high)
    if gender:
        df_cast = mask_value(df_cast, 'c_gender', gender)
    return df_cast


def mask_on_actor_edge_frequency(df_d3, edge_frequency_dict, min_threshold):
    actors_to_mask = [k for k, v in edge_frequency_dict.items() if v > min_threshold]
    mask = df_d3['source'].isin(actors_to_mask) & df_d3['target'].isin(actors_to_mask)
    return df_d3[mask].reset_index(drop=True)


def get_actor_co_star_dict(df_d3_masked):
    dic_merged = defaultdict(list)

    for source, target in zip(df_d3_masked['source'], df_d3_masked['target']):
        dic_merged[source].append(target)
        dic_merged[target].append(source)

    dic_source_target = dict(dic_merged)
    return dic_source_target


def find_common_movies(df, actor1, actor2):
    actor1_movies = set(df[df['c_name'] == actor1]['m_movie'])
    actor2_movies = set(df[df['c_name'] == actor2]['m_movie'])
    common_movies = actor1_movies.intersection(actor2_movies)
    return list(common_movies)


def get_poster_paths(df, common_movies, imdb_image_path):
    res = []
    for movie in common_movies:
        poster_path = df[df['m_movie'] == movie]['m_poster_path'].unique()[0]
        res.append((movie, imdb_image_path+poster_path))
    return res



