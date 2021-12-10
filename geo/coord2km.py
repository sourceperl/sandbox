#!/usr/bin/env python3

from geopy.distance import geodesic

POS_LILLE = '50.63679403420014, 3.0635113555071793'
POS_VALENCIENNES = '50.35799359468026, 3.523447645743657'

distance = geodesic(POS_LILLE.split(','), POS_VALENCIENNES.split(','))
print(f'Lille-Valenciennes: {distance.km:.2f} km')
