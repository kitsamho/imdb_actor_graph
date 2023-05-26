# Movie Graph Visualization

The Movie Graph Visualization app is a Streamlit application that allows users to explore and visualize the 
relationships between movies and actors. The app provides an interactive interface where users can filter movies based 
on release year and average rating, as well as filter actors based on popularity and gender. These filters help narrow 
down the dataset to specific movies and actors of interest.

Once the filters are applied, the app generates a movie graph visualization. The graph represents the connections 
between actors and movies, where actors are nodes and their collaborations in movies are represented by edges. The size 
of the nodes indicates the popularity of the actors, and the thickness of the edges represents the frequency of 
collaborations between actors.

Users can interact with the graph by adjusting the edge frequency threshold. This threshold allows users to control the 
level of collaboration between actors that is displayed in the graph. By manipulating the threshold, users can focus on 
highly collaborative actors or explore connections between less frequently collaborating actors.

In addition to the graph visualization, the app provides a section where users can select specific actors and their 
co-stars. The app then displays the movies in which the selected actors and co-stars have appeared together, along with 
their corresponding movie posters. This feature allows users to discover common movies and explore the filmography of 
their favorite actors.

Overall, the Movie Graph Visualization app provides a dynamic and interactive way to explore the relationships and 
collaborations between actors and movies. It enables users to uncover interesting connections, discover common films, 
and gain insights into the world of cinema.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/movie-graph-visualization.git
cd movie-graph-visualization
```

2. Create a python 3.1 environment

```
conda create --name imdb_actor_graph python=3.10
```

3. Install requirements
```
pip install -r requirements.txt
```

4. Run app
```
streamlit run app.py
```


## Project Structure

The project structure is as follows:

- `app.py`: Main Streamlit app script containing the code for filtering data and visualizing graphs.
- `common/`: Directory containing common utility functions for data loading, transformation, and visualization.
- `common/graph.py`: Module for graph-related calculations and metrics.
- `common/load.py`: Module for loading data from files.
- `common/show.py`: Module for displaying images and HTML plots.
- `common/streamlit_widgets.py`: Module for creating custom Streamlit widgets.
- `common/select.py`: Module for data selection and filtering.
- `common/transform.py`: Module for data transformation and manipulation.


## Data Sources
The data used in the Movie Graph Visualization app was sourced from The Movie Database (TMDB). The movie data and cast 
data were obtained by querying TMDB's API. While the code for querying the API is not included in the provided code 
snippet, if you find it useful, please feel free to reach out for further assistance.


## Data Formats
The data is stored in pickled data frames, which are cached locally in the repository. This format was chosen as it 
provides a convenient and efficient way to store and load the data. Since the data size was not too large, this 
approach was suitable for the project.


## Limitations
It's important to note that there are certain limitations to the data used in the app. The earliest available data 
is from 1990, and the overall dataset is skewed towards the past decade. This limitation is due to the data available 
through the TMDB API, which may not include comprehensive historical records. However, despite this limitation, 
the app still offers valuable insights into the relationships and collaborations between actors and movies based 
on the available data.