#!/usr/bin/env python3

""" Process all recent INGV flegrei events. """

import csv
import os
import urllib.error
from datetime import timezone
from urllib.request import urlopen

from dateutil.parser import ParserError, parse

# some const
CSV_FILE = 'events.csv'
CSV_URL = 'https://terremoti.ov.ingv.it/gossip/flegrei/events.csv'


# download csv file (if not already exist)
if not os.path.exists(CSV_FILE):
    print(f'file "{CSV_FILE}" does not exist -> download it')
    try:
        # request csv from web server
        resp = urlopen(CSV_URL, timeout=4.0)
        # extract
        with open(CSV_FILE, 'wb') as f:
            f.write(resp.read())
    except (urllib.error.URLError, ValueError) as e:
        print(f'error occur: {e!r}')


# process csv file
with open(CSV_FILE, 'r') as f:
    for event_d in csv.DictReader(f, delimiter=','):
        try:
            # extract and parse event fields
            evt_id = int(event_d['#EventID'])
            evt_dt = parse(event_d['Time']).replace(tzinfo=timezone.utc)
            try:
                evt_depth_km = round(float(event_d['Depth']), 1)
            except ValueError:
                evt_depth_km = None
            try:
                evt_magnitude = round(float(event_d['MD']), 1)
            except ValueError:
                evt_magnitude = None
            # show result (skip unset magnitude)
            if evt_magnitude is not None and evt_magnitude > 3.0:
                print(f'{str(evt_dt.astimezone()):35s} '
                      f'magnitude {str(evt_magnitude):>4s}  depth {str(evt_depth_km):>4s} km')
        except (ParserError, KeyError) as e:
            raise e
