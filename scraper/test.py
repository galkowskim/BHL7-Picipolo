from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Your_Name")

print(geolocator.geocode('360 3rd Ave, Brooklyn, NY').latitude)