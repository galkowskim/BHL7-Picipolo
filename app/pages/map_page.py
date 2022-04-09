import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from pages.utils import scraper
from pathlib import Path

# @st.experimental_memo(show_spinner=False, suppress_st_warning=True)
def app():
    df = scraper.load_data()

    col_dict = {
        'Brooklyn': 'red',
        'Manhattan': 'blue',
        'Bronx': 'green',
        'Queens': 'purple',
        'Staten Island': 'orange'
    }

    st.markdown('Map of NYC')

    map1 = folium.Map(
        location=[40.687759, -73.994781],
        zoom_start=12,
    )
    mCluster = MarkerCluster(name='example').add_to(map1)

    df.apply(lambda row:folium.Marker(location=[row["latitude"], row["longitude"]],
                                    icon=folium.Icon(color=col_dict[row['location']]),
                                    popup=row['location'] + '\n' + str(int(row['price'])) + '$').add_to(mCluster), axis=1)

    folium_static(map1)
    
    # heatmap
    # https://autogis-site.readthedocs.io/en/latest/notebooks/L5/02_interactive-map-folium.html 