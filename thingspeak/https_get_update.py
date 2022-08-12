#!/usr/bin/env python3

"""Basic Thingspeak update with an HTTPs GET request."""

import time
import urllib.error
from urllib.parse import urlencode
from urllib.request import urlopen
from private_data import API_KEY


# GET args
data = urlencode(dict(key=API_KEY, field1=round(time.monotonic(), 2)))

# send data to thingspeak
try:
    # do request
    resp = urlopen(f'https://api.thingspeak.com/update?{data}', timeout=4.0)
    # print request status
    try:
        # HTTP request return current entry ID or 0 on error
        entry_id = int(resp.read())
        if entry_id < 1:
            raise ValueError
        print(f'data write ok (entry ID: {entry_id})')
    except ValueError:
        print(f'unable to write data')
except urllib.error.URLError as e:
    print(f'urllib error occur: {e!r}')
