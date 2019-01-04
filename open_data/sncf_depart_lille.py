#!/usr/bin/env python3

from configparser import ConfigParser
from datetime import datetime
import dateutil.parser
import os
import requests
from requests.auth import HTTPBasicAuth

# read config
cnf = ConfigParser()
cnf.read(os.path.expanduser('../.private_config'))
api_key = cnf.get("sncf", "api_key")

auth = HTTPBasicAuth(api_key, "")

# play with sncf API : https://canaltp.github.io/navitia-playground/

# code UIC Lille Flandres 0087286005
#          Lille Europe   0087223263

# departures of train from "Lille Flandres"
stop_area = ":OCE:SA:87223263"
origin_dt = datetime.now().strftime("%Y%m%dT%H%M%S")
count = 10
url = "https://api.sncf.com/v1/coverage/sncf/stop_areas"
url += "/stop_area%s/departures?datetime=%s&count=%s"
url %= (stop_area, origin_dt, count)

# do request
r = requests.get(url, auth=auth)
d = r.json()

# print result
for dep in d['departures']:
    # compute delay
    dt_base = dateutil.parser.parse(dep["stop_date_time"]["base_departure_date_time"])
    dt_departure = dateutil.parser.parse(dep["stop_date_time"]["departure_date_time"])
    delay_min = round((dt_departure - dt_base).seconds/60)
    delay_str = "+ %i mn" % delay_min if delay_min >= 1 else "à l'heure"
    # format row
    t = (dt_base.strftime("%Hh%M"),
         delay_str,
         dep['display_informations']['headsign'],
         dep['display_informations']['commercial_mode'],
         dep['display_informations']['direction'])
    print("%-6s %-10s %8s %-8s %-45s" % t)
