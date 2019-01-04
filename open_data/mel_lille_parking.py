#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import dateutil.parser
import os
import requests
import thingspeak
import pandas as pd
import datetime
import schedule
import time


# some consts
NAN = float('nan')
OD_URL = 'https://opendata.lillemetropole.fr/api/records/1.0/search/'
PARK_REQ = '?dataset=disponibilite-parkings&rows=50'

# read config
cnf = ConfigParser()
cnf.read(os.path.expanduser('../.private_config'))
channel_id = cnf.get("mel_parking", "channel_id")
write_key = cnf.get("mel_parking", "write_key")

# set global options
pd.set_option('display.width', 120)


def job_park_update():
    # request Lille parking dataset
    try:
        park_raw_d = requests.get(OD_URL + PARK_REQ).json()
    except requests.exceptions.RequestException:
        return None

    # setup a dataframe
    park_df = pd.DataFrame(columns=['name', 'state', 'display', 'available', 'capacity', 'update', 'occupied'])
    park_df.index.name = 'id'

    # process data
    try:
        for record in list(park_raw_d['records']):
            # decode 'fields' part
            fields = dict(record['fields'])
            try:
                park_id = str(fields['id'])
                park_name = str(fields['libelle'])
                park_state = str(fields['etat'])
                park_display = str(fields.get('aff', ''))
                try:
                    park_update = dateutil.parser.parse(fields.get('datemaj', ''))
                except (KeyError, ValueError):
                    park_update = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
                park_available = float(fields.get('dispo', NAN))
                park_capacity = float(fields.get('max', NAN))
            except KeyError:
                # ignore this one, go next
                continue
            # process park data
            park_df.loc[park_id, 'name'] = park_name
            park_df.loc[park_id, 'state'] = park_state
            park_df.loc[park_id, 'display'] = park_display
            park_df.loc[park_id, 'available'] = park_available
            park_df.loc[park_id, 'capacity'] = park_capacity
            park_df.loc[park_id, 'update'] = park_update
    except (TypeError, KeyError):
        # global json fmt mismatch
        print('json not available or not valid')
        return None

    # add "occupied" ratio
    park_df['occupied'] = 100 - 100 * park_df['available']/park_df['capacity']

    # echo parking selection
    print(park_df.loc[['LIL0005', 'LIL0006', 'LIL0007', 'LIL0008']].sort_values(by='occupied', ascending=False))

    # update thingspeak
    channel = thingspeak.Channel(id=channel_id, write_key=write_key)
    try:
        ts_fields = dict()
        # Gare Lille Flandres
        ts_fields[1] = round(park_df.loc['LIL0005'].occupied, 1)
        # Gare Lille Europe
        ts_fields[2] = round(park_df.loc['LIL0008'].occupied, 1)
        # Tours
        ts_fields[3] = round(park_df.loc['LIL0007'].occupied, 1)
        # Euralille
        ts_fields[4] = round(park_df.loc['LIL0006'].occupied, 1)
        channel.update(ts_fields)
    except None:
        return None

# init
schedule.every(5).minutes.do(job_park_update)
job_park_update()

# loop
while True:
    schedule.run_pending()
    time.sleep(1.0)
