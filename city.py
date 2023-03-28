# import module
from geopy.geocoders import Nominatim

# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")


# Latitude & Longitude input
def get_city(Latitude, Longitude):
    Latitude = str(Latitude)
    Longitude = str(Longitude)

    location = geolocator.reverse(Latitude+","+Longitude)

    address = location.raw['address']

    # traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    return city

print(get_city(28.6139,77.2090))

