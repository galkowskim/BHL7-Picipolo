import csv
from dataclasses import fields

from .scraper import getPrices, Location

location = ['Brooklyn', 'Manhattan', 'Bronx', 'Queens', 'Staten Island']

with open('data.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(['location'] + [
        f.name
        for f in fields(Location)
    ])
    
    for l in location:
        page = 0
        while True:
            page += 1
            if page >= 10:
                break
            d = getPrices(l, page)
            if not d:
                break
            
            for dx in d:
                w.writerow([l] + [
                    getattr(dx, f.name)
                    for f in fields(Location)
                ])
            
            print(l, page)
            
        