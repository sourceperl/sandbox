#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import requests

url = 'https://services8.arcgis.com/rxZzohbySMKHTNcy/arcgis/rest/services/ind_hdf_agglo/FeatureServer/0/query' \
      '?where=1%3D1&outFields=date_ech,valeur,source,qualif,couleur,lib_zone,code_zone,type_zone' \
      '&returnGeometry=false&resultRecordCount=48&orderByFields=date_ech%20DESC&outSR=4326&f=json'

today_dt_date = datetime.today().date()

# call web api
atmo_raw_d = requests.get(url, timeout=5.0).json()

for record in atmo_raw_d['features']:
    # load record data
    r_lib_zone = record['attributes']['lib_zone']
    r_code_zone = record['attributes']['code_zone']
    r_ts = int(record['attributes']['date_ech'])
    r_dt = datetime.utcfromtimestamp(r_ts / 1000)
    r_value = record['attributes']['valeur']
    # retain today value
    if r_dt.date() == today_dt_date:
        print("%s  %16s (%5s)  indice : %s" % (r_dt, r_lib_zone, r_code_zone,  r_value))
