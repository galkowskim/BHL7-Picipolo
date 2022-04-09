import streamlit as st
from pages.utils import scraper


def app():
    df = scraper.load_data()
    st.write(df.head())
    # TODO must add text fields etc.