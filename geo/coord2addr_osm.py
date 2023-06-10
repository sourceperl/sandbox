#!/usr/bin/env python3

"""Nominatim OSM geocoder: convert address to coordinates and vice versa."""


from geopy.geocoders import Nominatim


# init geolocator
geolocator = Nominatim(user_agent='myapp')

# address to coordinates
from_addr = "1 Place De L'Hôtel De Ville, 59650 Villeneuve-d'Ascq"
location_point = geolocator.geocode(from_addr, exactly_one=True)
print(f'from address: {from_addr}')
print(f'get coordinates: ({location_point.latitude}, {location_point.longitude})')
print('')

# coordinate to address
coordinates = (50.63046, 3.06280)
rev_addr = geolocator.reverse(coordinates)
print(f'from coordinates: {coordinates}')
print(f'get address: {rev_addr.address}')
