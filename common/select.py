

def _mask_range(df, col, start, end):
    return df[(df[col] >= start) & (df[col] <= end)]


def _mask_value(df, col, value):
    return df[df[col] == value]


def _get_min_max_values(df, col, number_type):
    min_value, max_value = number_type(df[col].min()), number_type(df[col].max())
    return min_value, max_value

def _select_movie_data(df_movies,year_start, year_end=None,
                       # revenue_low=None, revenue_high=None,
                       # budget_low=None, budget_high=None,
                       vote_low=None, vote_high=None):


    if year_start:
        df_movies = _mask_range(df_movies, 'm_release_year', year_start, year_end)
    # if revenue_low:
    #     df_movies = _mask_range(df_movies, 'm_revenue', revenue_low, revenue_high)
    # if budget_low:
    #     df_movies = _mask_range(df_movies, 'm_budget', budget_low, budget_high)
    if vote_low:
        df_movies = _mask_range(df_movies, 'm_vote_average', vote_low, vote_high)

    return df_movies


def _select_gender(gender_choice):
    if gender_choice == 'Everyone':
        gender_mask = None
    elif gender_choice == 'Male':
        gender_mask = 2.0
    elif gender_choice == 'Female':
        gender_mask = 1.0
    return gender_mask
def _select_cast_data(df_cast,
                      popularity_low=None, popularity_high=None,
                      gender=None,
                      adult=None):

    if popularity_low:
        df_cast = _mask_range(df_cast, 'c_popularity', popularity_low, popularity_high)
    if gender:
        df_cast = _mask_value(df_cast, 'c_gender', gender)
    return df_cast


def _mask_on_actor_edge_frequency(df_d3, edge_frequency_dict, min_threshold):
    actors_to_mask = [k for k, v in edge_frequency_dict.items() if v > min_threshold]
    mask = df_d3['source'].isin(actors_to_mask) & df_d3['target'].isin(actors_to_mask)
    return df_d3[mask].reset_index(drop=True)


def _get_actor_co_star_dict(df_d3_masked):
    dic_source_target = dict(df_d3_masked.groupby('source')['target'].agg(lambda x: x.to_list()))
    dic_target_source = dict(df_d3_masked.groupby('target')['source'].agg(lambda x: x.to_list()))
    dic_source_target.update(dic_target_source)
    return dic_source_target


def _find_common_movies(df, actor1, actor2):
    actor1_movies = set(df[df['c_name'] == actor1]['m_movie'])
    actor2_movies = set(df[df['c_name'] == actor2]['m_movie'])
    common_movies = actor1_movies.intersection(actor2_movies)
    return list(common_movies)


def _get_poster_paths(df, common_movies):
    res = []
    base_url = 'https://image.tmdb.org/t/p/original'
    for movie in common_movies:
        poster_path = df[df['m_movie'] == movie]['m_poster_path'].unique()[0]
        res.append((movie, base_url+poster_path))
    return res



