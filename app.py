import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from d3blocks import D3Blocks

st.set_page_config(layout="wide")
path = '/Users/saho/PycharmProjects/d3blocks_streamlit/test.html'

d3 = D3Blocks()

@st.cache_data
def get_df():
    df = d3.import_example('energy')
    return df
df = get_df()

st.slider(0,)
df_mask = df[df.weight >= 1]
st.dataframe(df_mask)

d3.d3graph(df_mask,title='dsfsdf')
save_path = '/Users/saho/Documents/sam/imdb_actor_graph/temp/html_new.html'
d3.D3graph.show(filepath=save_path)



# Load the HTML file
with open(save_path, "r") as f:
    html_code = f.read()

# Render the HTML file using the `html` function
st.header('Graph Test')
st.components.v1.html(html_code, width=1200, height=1200)




