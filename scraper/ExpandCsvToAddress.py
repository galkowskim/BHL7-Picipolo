from geopy.geocoders import Nominatim
import csv
from dataclasses import fields
from .scraper import Location

geolocator = Nominatim(user_agent="Your_Name")

with open('data.csv', 'r') as f1, open('dataWithAddress.csv', 'w') as f2:
    
    line = f1.readline()
    line = f1.readline()
    line = f1.readline()
    
    w = csv.writer(f2)
    w.writerow(['location'] + [
        f.name
        for f in fields(Location)
    ] + ['address'])
    
    count = 0
    
    while count != 2:
        if line is not None:
            count = 0
            elementy = line.split(',')
        array = line.split(',')
        text = array[1] + ', ' + array[2]
        print(text)
        text = geolocator.reverse(text).address
        w.writerow([el for el in elementy] + [text])
        line = f1.readline()
        count += 1
        
    





