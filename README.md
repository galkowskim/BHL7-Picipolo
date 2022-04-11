# Repository for Best Hacking League 7 challenge in Artificial Intelligence

## Authors

- Wiktor Jakubowski
- Mikołaj Gałkowski
- Hubert Bujakowski
- Łukasz Tomaszewski

## Problem

New York City as a centre of one of the most populated aglomerations worldwide poses a great case study of large metropolies functioning. Data about real estate prices and details in NYC in 2021 can let us deepen our understanding of the process of forming property prices in huge, overcrowded cities. Analyze the dataset you are provided with and find the use in real world of the knowledge you gained during this process.

## Solution and implementation

Web Application displaying prices of real estates in near location and predicting whether they are over-priced, realiable or under-priced. Application targets broad customer group as it could be used both by real estate buyers seeking reliable information about housing prices in certain location as well as real estate agents wanitng to confront their price with the one optimized by Artificial Intelligence models.

- Optimized Machine Learning model called Random Forest Regressor which predicted the price of property based on severl features like longitude, latitude, metrage using Sci-kit Learn Python library
- Constructed Web Scrapper in Python using Beautiful Soup and Request packages in order to retrieve more data about housing market prices in NYC Technopolis from housing market sites (Zillow.com, Trulia.com)
- Created Web App prototype in Streamlit, displaying the map with real estate prices in NYC using Folium library
