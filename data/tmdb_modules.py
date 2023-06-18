import numpy as np
import concurrent.futures
import threading
import tmdbsimple as tmdb
import pandas as pd
import concurrent.futures

class MultiThreading:

    def __init__(self, threads, iteration_list, output=[]):
        self.threads = threads
        self.output = output
        self.iteration_list = iteration_list

    def multi_thread_compile(self, thread_count, function):

        """a function that compiles an iteration list to prepare
        multi threadding"""

        jobs = []

        # distribute iteration list to batches and append to jobs list
        batches = [i.tolist() for i in np.array_split(self.iteration_list, thread_count)]

        for i in range(len(batches)):
            jobs.append(threading.Thread(target=function, args=[batches[i]]))

        return jobs

    def multi_thread_execute(self, jobs):

        """executes the multi-threading loop"""

        # Start the threads
        for j in jobs:
            j.start()

        # Ensure all of the threads have finished
        for j in jobs:
            j.join()
        return

    def Run(self, function):

        jobs = self.multi_thread_compile(self.threads, function)
        self.multi_thread_execute(jobs)


def get_movie_payload():
    movie_payload = {'keywords': {'movie_response': [], 'cols': ['id', 'keywords'], 'results_parsed': []},
                     'reviews': {'movie_response': [], 'cols': ['id', 'results'], 'results_parsed': []},
                     'info': {'movie_response': [],
                              'cols': ['id', 'budget', 'revenue', 'genres', 'production_countries', 'tagline'],
                              'results_parsed': []}}

    return movie_payload


class TMDBMovieScraper:
    def __init__(self, years_check: list):
        """
        Initializes the TMDBMovieScraper class with a list of years to iterate over for querying movie data from TMDB.

        Args:
            years_check (list): List of years to iterate over for querying movie data.
        """
        self.discover_api = tmdb.Discover()  # Instantiate tmdb.Discover module
        self.years_check = years_check  # List of years to iterate over
        self.discover_results = []  # Results for movie discovery
        self.movie_payload = get_movie_payload()  # Get an empty movie payload

    def _check_page_counts(self, discover_api, year: int):
        """
        Helper method to check the number of response pages to iterate over for a specific year.

        Args:
            discover_api (tmdb.Discover): Instance of tmdb.Discover module.
            year (int): Year to query.

        Returns:
            total_pages_to_loop (int): Number of response pages to iterate over.
        """
        total_pages_to_loop = discover_api.movie(year=year, page=1)['total_pages']
        return total_pages_to_loop

    def _request_discover_data(self, years_check: list):
        """
        Helper method to query movie data using the discover API.

        Args:
            years_check (list): List of years to iterate over for querying movie data.
        """
        for year in years_check:  # For each year
            try:
                total_pages_to_loop = self._check_page_counts(self.discover_api, year)  # Check number of pages

                for page in range(1, total_pages_to_loop):  # For each page in a given year
                    try:
                        movie_results = self.discover_api.movie(primary_release_year=year,
                                                                page=page,
                                                                with_original_language='en',
                                                                include_adult=False,
                                                                vote_count_gte=100)

                        self.discover_results.append(movie_results['results'])  # Append results to a list
                    except:
                        pass
            except:
                pass

    def _request_movie_data(self, movie_ids: list):
        """
        Helper method to query movie details using movie IDs.

        Args:
            movie_ids (list): List of movie IDs.
        """
        for movie_id in movie_ids:  # Iterate over each movie ID
            try:
                for k, v in self.movie_payload.items():  # Iterate over each key and value in payload
                    v['movie_response'] = self._get_film_responses(movie_id, k)  # Get film response from API instance

                    v['results_parsed'].append(self._parse_movie_response(v['movie_response'], v['cols']))
            except:
                pass

    def _transform_discover_results(self, discover_results):
        """
        Helper method to transform discover results into a DataFrame.

        Args:
            discover_results: Results from movie discovery.

        Returns:
            discover_df (pd.DataFrame): Transformed DataFrame of discover results.
        """
        discover_df = pd.concat(pd.DataFrame(i) for i in discover_results)
        discover_df = discover_df[
            ['id', 'title', 'overview', 'popularity', 'release_date', 'vote_average', 'poster_path']]
        discover_df['release_year'] = discover_df['release_date'].apply(lambda x: x.split("-")[0])

        return discover_df.set_index('id')

    def _transform_movie_results(self):
        """
        Helper method to transform movie results into a DataFrame.

        Returns:
            movie_df (pd.DataFrame): Transformed DataFrame of movie results.
        """
        results = [pd.DataFrame(self.movie_payload[k]['results_parsed']).set_index('id') for k, v in
                   self.movie_payload.items()]
        movie_df = results[0].join(results[1]).join(results[2])
        return movie_df

    def _get_movie_ids(self, discover_dataframe):
        """
        Helper method to retrieve movie IDs from the discover DataFrame.

        Args:
            discover_dataframe (pd.DataFrame): DataFrame of discover results.

        Returns:
            movie_ids (list): List of movie IDs.
        """
        movie_ids = list(discover_dataframe.index)
        return list(set(movie_ids))

    def _get_film_response(self, movie_id):
        """
        Helper method to get film response from TMDB API.

        Args:
            movie_id: ID of the movie.

        Returns:
            film_response: Film response from TMDB API.
        """
        film_response = tmdb.Movies(movie_id)
        return film_response

    def _get_film_responses(self, movie_id, data_stream='info'):
        """
        Helper method to get film responses based on data stream type.

        Args:
            movie_id: ID of the movie.
            data_stream (str): Data stream type.

        Returns:
            film_response: Film response based on the specified data stream.
        """
        film_response = self._get_film_response(movie_id)
        if data_stream == 'reviews':
            return film_response.reviews()
        elif data_stream == 'info':
            return film_response.info()
        elif data_stream == 'keywords':
            return film_response.keywords()

    def _parse_movie_response(self, response_dic, cols_needed):
        """
        Helper method to parse movie response based on the required columns.

        Args:
            response_dic: Movie response dictionary.
            cols_needed (list): Required columns.

        Returns:
            parsed_response (dict): Parsed movie response containing the required columns.
        """
        parsed_response = {k: v for k, v in response_dic.items() if k in cols_needed}
        return parsed_response

    def _dict_to_list(self, x, key_name):
        """
        Helper method to convert a dictionary to a list based on a specific key.

        Args:
            x: Input dictionary.
            key_name (str): Key name.

        Returns:
            converted_list: List converted from the dictionary.
        """
        try:
            return [i[key_name] for i in x]
        except:
            return x

    def _merge_clean_and_filter(self):
        """
        Helper method to merge, clean, and filter the movie DataFrame.

        Returns:
            df (pd.DataFrame): Merged, cleaned, and filtered DataFrame.
        """
        self.df = self.discover_df.join(self.movie_df)

        cols = {'results': 'content', 'genres': 'name', 'production_countries': 'name', 'keywords': 'name'}

        for k, v in cols.items():
            self.df[k] = self.df[k].apply(lambda x: self._dict_to_list(x, v))

        self.df = self.df.rename(columns={'id': 'tmdb_id', 'title': 'movie'})

        return self.df

    def get_movies(self):
        """
        Method to initiate the data retrieval process.
        """
        print(f'Getting data for {self.years_check}')
        mt = MultiThreading(10, self.years_check, None)
        mt.Run(self._request_discover_data)

        self.discover_df = self._transform_discover_results(self.discover_results)
        self.movie_ids = self._get_movie_ids(self.discover_df)
        print(f'Getting movie data for {len(self.movie_ids)} movies..')
        mt = MultiThreading(10, self.movie_ids, None)
        mt.Run(self._request_movie_data)

        self.movie_df = self._transform_movie_results()
        self.df_final = self._merge_clean_and_filter()
        print('Done')

        return self.df_final


class TMDBCastCrewScraper(TMDBMovieScraper):

    def __init__(self, movie_ids: list, popularity_threshold=1, max_threads=30):
        self.movie_ids = movie_ids
        self.cast_results = []
        self.crew_results = []
        self.popularity_threshold = popularity_threshold
        self.max_threads = max_threads

    def _append_data_to_list(self, list_dic_results, popularity_threshold, results, movie_id):
        for dic in list_dic_results:
            if dic['popularity'] >= self.popularity_threshold:
                dic['tmdb_id'] = movie_id
                results.append(dic)

    def _get_cast_crew_for_movie(self, movie_id):
        try:
            film_response = self._get_film_response(movie_id)
            #             crew_dic_list = film_response.credits()['crew']
            cast_dic_list = film_response.credits()['cast']
            #             self._append_data_to_list(crew_dic_list,self.popularity_threshold,self.crew_results,movie_id)
            self._append_data_to_list(cast_dic_list, self.popularity_threshold, self.cast_results, movie_id)

        except:
            pass

    def _request_cast_crew_data(self, movie_ids):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for movie_id in movie_ids:
                futures.append(executor.submit(self._get_cast_crew_for_movie, movie_id))
            concurrent.futures.wait(futures)
        return

    def get_cast_crew(self):
        self._request_cast_crew_data(self.movie_ids)
        self.df = pd.DataFrame(self.cast_results)
        return self.df









