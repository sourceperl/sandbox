#!/usr/bin/env python3

"""Influxdb select with CSV export (and decode) from an HTTP GET request."""

import csv
from pprint import pprint
import urllib.error
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# format URL for write data
db_query = 'SELECT * FROM "metars" GROUP BY * ORDER BY time DESC LIMIT 2'
query_args = urlencode(dict(db='mydb', epoch='s', q=db_query))
url = f'http://192.168.1.60:8086/query?{query_args}'
headers = {'Accept': 'application/csv'}

# Request data from influxdb
try:
    # do request
    resp = urlopen(Request(url, headers=headers), timeout=4.0)
    # process response
    raw_csv_l = resp.read().decode().splitlines()
    csv_dr = csv.DictReader(raw_csv_l)
    # show results
    print('RAW CSV as list:')
    pprint(raw_csv_l)
    print('')
    print('Decoded CSV as list of dict:')
    pprint(list(csv_dr))
except urllib.error.URLError as e:
    print(f'error occur: {e!r}')
