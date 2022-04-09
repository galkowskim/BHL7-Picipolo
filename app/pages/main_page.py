import streamlit as st
from pages.utils import scraper


def app():
    df = scraper.load_data()
    #st.write(df.head())

    longitude = st.text_input('Enter longitude coordinates of the property', '40.70')
    latitude = st.text_input('Enter latitude coordinates of the property', '60.30')
    property_type = st.text_input('Enter property type', 'Office')
    building_class = st.text_input('Enter property building class', 'R')
    year = st.text_input('Enter year the property was built in', '1997')

    # TODO
    # wczytać model
    # wyliczyć predykcyjną cene i zwrócić na ekran:
    model = float(longitude) * 2 # próba - potem sie usunie i zamieni wynikiem z modelu

    price = st.text(f"Predicted price of your real estate is: {model}")
