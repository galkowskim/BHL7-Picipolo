import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd

from pathlib import Path

datapath = Path(__file__).parents[1].joinpath('data', 'data.csv')
df = pd.read_csv(datapath)

col_dict = {
    'Brooklyn': 'red',
    'Manhattan': 'blue',
    'Bronx': 'green',
    'Queens': 'purple',
    'Staten Island': 'orange'
}

st.title('Map of NYC')
# st.write(df.head())

map1 = folium.Map(
    location=[40.687759, -73.994781],
    zoom_start=12,
)
mCluster = MarkerCluster(name='example').add_to(map1)

df.apply(lambda row:folium.Marker(location=[row["latitude"], row["longitude"]],
                                  icon=folium.Icon(color=col_dict[row['location']]),
                                  popup=row['location'] + '\n' + str(int(row['price'])) + '$').add_to(mCluster), axis=1)

folium_static(map1)

# map1.save('output.html')
