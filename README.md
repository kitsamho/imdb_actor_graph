![Image Description](assets/hollywood.jpeg)


# TMDB Actor Graph Streamlit App

The TMDB Actor Graph streamlit app is a multi tab application that facilitates analysis of Hollywood actors
based on their collaborations in movies. The app also calculates graph metrics to provide 
insights into the importance and connectivity of actors. Additionally, users can explore common movies between selected 
actors and their co-stars, with movie posters displayed for interactive and visual exploration. 

---

### Graph
Once the filters are applied, the app generates a graph visualisation implementing [d3Blocks.](https://d3blocks.github.io/d3blocks/pages/html/index.html) 
The graph represents the connections between actors and movies, where actors are nodes and their collaborations in 
movies are represented by edges. The thickness of the edges represents the frequency of collaborations between actors.

Users can interact with the graph by adjusting the edge frequency threshold. This threshold allows users to control the 
level of collaboration between actors that is displayed in the graph. By manipulating the threshold, users can focus on 
highly collaborative actors or explore connections between less frequently collaborating actors.

### Graph Metrics

In the Streamlit app, after applying filters, an undirected graph is constructed using NetworkX. By calculating 
metrics such as betweenness centrality, degree centrality, eigenvector centrality, and clustering coefficients we can 
gain insights into the relative importance, influence, and connectivity of each actor within the network.

 
### Common Movies
In addition to the graph visualisation, the app provides a section where users can select specific actors and their 
co-stars. The app then displays the movies in which the selected actors and co-stars have appeared together, along with 
their corresponding movie posters. This feature allows users to discover common movies and explore the filmography of 
their favorite actors.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/movie-graph-visualization.git
cd movie-graph-visualization
```

2. Create a python 3.10.10 environment

```
conda create --name imdb_actor_graph python=3.10.10
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

- The ```app.py``` script imports the necessary modules from the common package.
- The load module provides functions such as load_cached_file and load_config for loading cached files and configuration 
data, respectively.
- The transform module provides classes such as ```DataLoader```, ```MovieCastTransformer```, ```D3Transformer```, and 
```ActorGraphTransformer```
for data transformation tasks.
- The show module offers functions like ```cache_d3_network_plot```, ```plot_html```, ```display_image_grid```, and 
- ```plot_graph_metrics```
for visualizing data.
- The ```select.py``` module provides functions for filtering and selecting specific data.
- The ```streamlit_widgets.py``` module contributes the custom Streamlit widget ```st_expander``` for expanding and 
- collapsing sections of the app interface, enhancing user experience and navigation within the app.

## Data Sources
The data used in the app was sourced from [The Movie Database (TMDB)](https://developer.themoviedb.org/docs). 
The movie data and cast data were obtained by querying TMDB's API (which is free to use and has very user-friendly
limits). 


## Data Formats
The data is stored in pickled data frames, which are cached locally in the repository. This format was chosen as it 
provides a convenient and efficient way to store and load the data. Since the data size was not too large, this 
approach was suitable for the project. In future to scale up the app, we would persist the data to a warehouse and 
implement relevant queries to collect data. That comes with cost, and for demo purposes, local pickled static data sets
are sufficient to make the point.


## Limitations
It's important to note that there are certain limitations to the data used in the app. The earliest available data 
is from 1990, and the overall dataset is skewed towards the past decade. This limitation is due to the data available 
through the TMDB API, which may not include comprehensive historical records. However, despite this limitation, 
the app still offers valuable insights into the relationships and collaborations between actors and movies based 
on the available data.


## Contributions

Contributions to this project are welcome and encouraged. If you have ideas for different features or if there are bugs. 

If you would like to contribute, you can follow these steps:

- Fork the repository on GitHub.
- Create a new branch with a descriptive name for your contribution.
- Make your desired changes or additions to the codebase.
- Test your changes to ensure they are functioning correctly.
- Commit and push your changes to your forked repository.
- Open a pull request (PR) against the main repository.
- Provide a clear and descriptive explanation of your changes in the PR description.
