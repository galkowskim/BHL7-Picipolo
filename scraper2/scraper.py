import requests
import pandas as pd
import re
import csv
import numpy as np
import random
import string
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from urllib.parse import urlparse

df = pd.DataFrame(
    columns=['address', 'price', 'property type', 'building size', 'year built', 'building class', 'lat', 'lon'])


def GET_UA():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0", \
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", \
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36" \
        ]

    return random.choice(uastrings)


def parse_url(url):
    headers = {'User-Agent': GET_UA()}
    content = None

    try:
        response = requests.get(url, headers=headers)
        ct = response.headers['Content-Type'].lower().strip()

        if 'text/html' in ct:
            content = response.content
            soup = BeautifulSoup(content, "lxml")
        else:
            content = response.content
            soup = None

    except Exception as e:
        print("Error:", str(e))

    return content, soup, ct


def parse_internal_links(soup, current_page):
    return [a['href'].lower().strip() for a in soup.find_all('a', href=True) if
            urlparse(a['href']).netloc == urlparse(current_page).netloc]


def process_search_result(result_url):
    headers = {'User-Agent': GET_UA()}
    results_dict = {}
    response = requests.get(result_url, headers=headers)
    if response.status_code == 200:
        results_dict['PropertyURL'] = result_url
        property_html = response.text
        soup = BeautifulSoup(property_html, features="html.parser")

        # Get Property Address from title
        title_text = soup.find("title").string.strip()
        match = re.match(r'^.+[0-9]+', title_text, re.I)
        if match:
            title_text = match.group()

        results_dict['Address'] = title_text

        # Get all the pictures for the property
        image_urls = []
        image_elements = soup.find_all("i", {"class": "ln-icon-zooming"})
        for image_element in image_elements:
            url = image_element.parent.find("img").get("src")
            image_urls.append(url)

        # Use first image as result image for now
        if len(image_urls) > 0:
            results_dict['ImageURL'] = image_urls[0]

        # Process attribute data for the result
        property_data_table = soup.find("table", {"class": "property-data"})
        for row in property_data_table.find_all('tr'):
            try:
                cells = row.find_all('td')
                for i in range(len(cells)):
                    # The cells follow a pattern of Property Name --> Property Value
                    if i % 2 != 0:  # Property Title
                        results_dict[cells[i - 1].string.strip()] = cells[i].string.strip()
            except:
                continue

        # Process Unit Mix Information Section
        property_unit_mix_table = soup.find("table", {"class": "property-data summary"})
        if property_unit_mix_table:
            unit_mix_table_headers = property_unit_mix_table.find_all("th")
            unit_mix_table_values = property_unit_mix_table.find_all("td")
            for header_index in range(len(unit_mix_table_headers)):
                header_name = unit_mix_table_headers[header_index].text.strip()
                header_value = unit_mix_table_values[header_index].text.strip()
                results_dict['MIX_INFO_%s' % header_name] = header_value

    else:
        print("Failed to parse property for %s" % result_url)

    return results_dict


content, soup, ct = parse_url(
    "https://www.loopnet.com/search/office-buildings/brooklyn-ny/for-sale/?sk=1c436c3499898580bdacd4e393ed2494&bb=2k3mttjg3Hul19i8pE")

results = []

properties = soup.find_all('article')
if len(properties) > 0:
    for property in properties:
        property_url = property.find("header").find("a").get("href")
        processed_result = process_search_result(property_url)
        results.append(processed_result)


# print(results[0])


def scrape_page(r):
    headers = {'User-Agent': GET_UA()}
    results_dict = {}
    response = requests.get(r, headers=headers)
    if response.status_code == 200:
        property_html = response.text
        soup = BeautifulSoup(property_html, features="html.parser")

        myh1 = soup.find_all("h1", {"class": "breadcrumbs__crumb breadcrumbs__crumb-title"})
        # print(myh1[0].text) # adres, mamy to

        tables = soup.find("table", {'class': "property-data featured-grid"})

        for row in tables.find_all('tr'):

            columns = row.find_all('td')
            for i in range(0, len(columns), 2):
                results_dict[columns[i].text.strip()] = columns[i + 1].text.strip()

        print(results_dict)
        return results_dict, myh1[0].text
        

locator = Nominatim(user_agent="myGeocoder")

if len(results) > 0:
    with open('data_scrapped.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['price'] + ['property type'] + ['building size'] +
                   ['year built'] + ['building class'] + ['lat'] + ['lon'])
        for r in results:
            row_results, addr = scrape_page(r['PropertyURL'])
            for key, value in row_results.items():
                row_results[key] = value.replace('\t', '').replace('\n', '')
            try:
                att_price = int(row_results['Price'][1:].replace(',', ''))
            except:
                att_price = np.nan
            try:
                att_property_type = row_results['Property Type']
            except:
                att_property_type = np.nan
            try:
                att_building_size = int(row_results['Building Size'].replace(' ', '')[0].strip())
            except:
                att_building_size = np.nan
            try:
                att_year_built = int(row_results['Year Built'].strip())
            except:
                att_year_built = np.nan
            try:
                att_building_class = row_results['Building Class']
            except:
                att_building_class = np.nan
            try:
                location = locator.geocode(addr)
            except:
                att_log = np.nan
                att_lat = np.nan
            try:
                att_log = float(location.longitude)
            except:
                att_log = np.nan
            try:
                att_lat = float(location.latitude)
            except:
                att_lat = np.nan
            w.writerow([att_price] + [att_property_type] + [att_building_size]
                       + [att_year_built] + [att_building_class] + [att_lat] + [att_log])
