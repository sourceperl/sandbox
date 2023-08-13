# from https://www.geeksforgeeks.org/how-to-track-iss-international-space-station-using-python/

import json 
import turtle
import urllib.request
import time


# init background image
screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic('data\map.gif')
screen.register_shape('data\iss.gif')

# init ISS as turtle
iss = turtle.Turtle()
iss.shape('data\iss.gif')
iss.setheading(45)
iss.penup()

while True:
    # request the current position of the ISS
    url = 'http://api.open-notify.org/iss-now.json'
    response = urllib.request.urlopen(url)
    # check HTTP status
    if response.status == 200:
        try:
            result = json.loads(response.read())
            # extract json data
            iss_position = result['iss_position']
            iss_lat = float(iss_position['latitude'])
            iss_lon = float(iss_position['longitude'])
            # update ISS location
            print(f'ISS pos: {iss_lat:0.04f}, {iss_lon:0.04f}')
            iss.goto(iss_lon, iss_lat)
        except Exception as e:
            print(f'an error occur: {e}')
    # reload in 5s
    time.sleep(5.0)
