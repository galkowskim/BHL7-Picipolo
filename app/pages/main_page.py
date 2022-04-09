import pandas as pd
import streamlit as st
from pages.utils import scraper
import pickle

def app():
    df = scraper.load_data()
    #st.write(df.head())

    longitude = st.text_input('Enter longitude coordinates of the property', '40.70')
    latitude = st.text_input('Enter latitude coordinates of the property', '60.30')
    region = st.selectbox(
     'Select area region of NYC the property is located in',
     ('Brooklyn', 'Bronx', 'Manhattan', 'Queens', 'Staten Island'))
    year = st.text_input('Enter year the property was built in', '1997')
    
    loaded_model = scraper.load_model()
    if(st.button("Predict")):
        
        x = pd.DataFrame(columns = ['EXT_E','EXMPTCL_X1','EXMPTCL_X5','YEAR_2018','Borough_BRONX','Borough_BROOKLYN','Borough_MANHATTAN','Borough_STATEN IS',
    'BLDGCL_B3','BLDGCL_C0','BLDGCL_Other','BLDGCL_V0','TAXCLASS_1','TAXCLASS_1A','TAXCLASS_1C','TAXCLASS_2','TAXCLASS_2A',
    'TAXCLASS_2B','TAXCLASS_2C','TAXCLASS_4','STORIES','AVTOT','EXTOT','EXCD1','Latitude','Longitude','LOTAREA','BLDAREA'])
        x.loc[0] = [0,0,0, 1 if year == 2018 else 0,1 if region == "Bronx" else 0, 1 if region == "Brooklyn" else 0,
                1 if region == "Manhattan" else 0, 1 if region == "Staten Island" else 0,0.017101,0.046281,0.353863,0.017340,
            0.499402,0.097345,0.000478,0.218608,0.019373,0.010883,0.018775,0.111337,0.119540,0.001942,0.001681,0.107027,latitude,longitude, 0.145783, 0.105869]
        result = loaded_model.predict(x)
     # próba - potem sie usunie i zamieni wynikiem z modelu

        st.text(f"Predicted price of your real estate is: {int(result)}$")
