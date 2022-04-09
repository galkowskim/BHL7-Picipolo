from geopy.geocoders import Nominatim
import csv
from dataclasses import fields
from .scraper import Location

geolocator = Nominatim(user_agent="")

with open('data.csv', 'r') as f1, open('dataWithAddress.csv', 'w', newline = '') as f2:
    
    line = f1.readline()
    line = f1.readline()
    line = f1.readline()
    
    w = csv.writer(f2)
    w.writerow(['location'] + [
        f.name
        for f in fields(Location)
    ] + ['address'])
    
    count = 0
    
    while line:
        print(count)
        count += 1
        elementy = line.split(',')
        array = line.split(',')
        text = array[1] + ', ' + array[2]
        text = geolocator.reverse(text).address
        text = text.split(', ')
        text = text[1] + ' ' + text[0]
        w.writerow([el.strip() for el in elementy] + [text])
        line = f1.readline()
        
    





