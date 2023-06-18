![Image Description](../streamlit_app/assets/tmdb_logo.png)
---

## TMDB Movie Data 

This folder contains code for querying movie data from the TMDB (The Movie Database) API. 
It includes two classes: `TMDBMovieScraper` and `TMDBCastCrewScraper`. The TMDBMovieScraper class is responsible for 
querying movie data, while the TMDBCastCrewScraper class extends the functionality to retrieve cast and crew information 
for movies. 

### tmdbsimple

When building these classes, we implemented the [tmdbsimple](https://github.com/celiao/tmdbsimple) library, which 
provided convenient methods for accessing TMDB API endpoints. This library simplifies the process of retrieving data by 
handling HTTP requests and authentication

### TMDB API Key

Information on how to get an API key can be found at [The Movie Database (TMDB)](https://developer.themoviedb.org/docs). 
The API is free to use and has user-friendly rate limiting. 
---

### Usage

Import the necessary modules
```
import tmdbsimple as tmdb
import pandas as pd
```

Instantiate the TMDBMovieScraper class and call the `get_movies` method to retrieve movie data:
```
movies = TMDBMovieScraper(years_check=[2022,2023])
df_movies = movies.get_movies()
```

Instantiate the TMDBCastCrewScraper class and provide a list of movie IDs from the df_movies dataframe

```
cast = TMDBCastCrewScraper(df_movies.index)
df_cast = cast.get_cast_crew()
```

### Multithreading

Both classes implement multithreading to speed up the data retrieval process. The number of threads can be 
controlled by adjusting the max_threads parameter.

### Example Usage

Please refer to the provided Jupyter Notebook for a complete example workflow and usage details.

