#!/usr/bin/env python3

""" Request and process data about campi flegrei events from INGV. """

import csv
from datetime import timezone
import urllib.error
from urllib.request import urlopen
from dateutil.parser import parse, ParserError


# some const
DATA_URL = 'https://terremoti.ov.ingv.it/gossip/flegrei/2025/events.csv'


try:
    # request CSV data from web server
    resp = urlopen(DATA_URL, timeout=4.0)
    lines_l = resp.read().decode().splitlines()
    # extract
    for row in csv.DictReader(lines_l, delimiter=','):
        try:
            event_id = int(row['#EventID'])
            event_dt = parse(row['Time']).replace(tzinfo=timezone.utc)
            try:
                depth_km = float(row['Depth'])
            except ValueError:
                depth_km = None
            try:
                mag = float(row['MD'])
            except ValueError:
                mag = None
            if mag and mag > 2.0:
                event_dt_str = event_dt.astimezone().isoformat(timespec='seconds')
                print(f'{event_dt_str} magnitude: {mag} (depth: {depth_km:.1f} km)')
        except (ParserError, KeyError):
            pass
except (urllib.error.URLError, ValueError) as e:
    print(f'error occur: {e!r}')
