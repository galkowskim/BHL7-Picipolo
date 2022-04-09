import random
import requests
from bs4 import BeautifulSoup

results = {'PropertyURL': 'https://www.loopnet.com/Listing/3175-Emmons-Ave-Brooklyn-NY/25410827/', 'Address': '3175 Emmons Ave, Brooklyn, NY 11235'}

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]
 
    return random.choice(uastrings)

def scrape_page(r):
    headers = {'User-Agent': GET_UA()}
    results_dict = {}
    response = requests.get(r['PropertyURL'], headers=headers)
    if response.status_code == 200:
        #results_dict['PropertyURL'] = r['PropertyURL']
        property_html = response.text
        soup = BeautifulSoup(property_html, features="html.parser")
        
        myh1 = soup.find_all("h1", {"class": "breadcrumbs__crumb breadcrumbs__crumb-title"})
        print(myh1[0].text) # adres, mamy to
        
        tables = soup.find("table", {'class': "property-data featured-grid"})
        
        for row in tables.find_all('tr'):
            
            columns = row.find_all('td')
            for i in range(0, len(columns), 2):
                results_dict[columns[i].text.strip()] = columns[i+1].text.strip()
                
        return results_dict
                    
                    
                    
        
            
# if(columns != []):
#     neighborhood = columns[0].text.strip()
#     zone = columns[1].text.strip()
#     area = columns[2].span.contents[0].strip('&0.')
#     population = columns[3].span.contents[0].strip('&0.')
#     density = columns[4].span.contents[0].strip('&0.')
#     homes_count = columns[5].span.contents[0].strip('&0.')

#     df = df.append({'Neighborhood': neighborhood,  'Zone': zone, 'Area': area, 'Population': population, 'Density': density, 'Homes_count': homes_count}, ignore_index=True)
    

tmp = scrape_page(results)