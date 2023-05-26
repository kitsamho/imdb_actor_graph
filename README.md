# Movie Graph Visualization

This project is a Streamlit app that allows users to visualize movie graphs and explore the relationships between actors 
and movies.

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

## Usage

Set Streamlit page configuration by modifying the st.set_page_config() line in app.py.
Define the file paths for the movie and cast data in app.py. Make sure the data files are in the specified paths.
Customize the movie and actor filters in the sidebar by modifying the corresponding sections in app.py.
Run the Streamlit app as described in the installation steps.
Use the sliders and select boxes in the sidebar to filter the movie and actor data.
Explore the movie graph visualization in the "Graph Visualization" section. Adjust the edge frequency threshold using the slider to customize the graph.
View the films starred in by selecting actors and co-stars in the "Films Starred In" section. The corresponding movie posters will be displayed.

## Project Structure

The project structure is as follows:

app.py: Main Streamlit app script containing the code for filtering data and visualizing graphs.
common/: Directory containing common utility functions for data loading, transformation, and visualization.
common/graph.py: Module for graph-related calculations and metrics.
common/load.py: Module for loading data from files.
common/show.py: Module for displaying images and HTML plots.
common/streamlit_widgets.py: Module for creating custom Streamlit widgets.
common/select.py: Module for data selection and filtering.
common/transform.py: Module for data transformation and manipulation.