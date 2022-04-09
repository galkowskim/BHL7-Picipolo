import streamlit as st

from multipage import MultiPage
from pages import main_page, map_page

app = MultiPage()

st.title("NYC Analysis")

app.add_page('Main Page', main_page.app)
app.add_page('Map Page', map_page.app)


if __name__ == '__main__':
    app.run()
    