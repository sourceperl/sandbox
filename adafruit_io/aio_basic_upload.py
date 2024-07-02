#!/usr/bin/env python3

"""Basic io.adafruit.com update with an HTTPs POST request."""

import urllib.error
from urllib.request import urlopen, Request
from private_data import AIO_USER, AIO_KEY


# send data to io.adafruit.com
try:
    # feed value
    feed = 'test'
    value = 42.2
    # build request
    req = Request(f'https://io.adafruit.com/api/v2/{AIO_USER}/feeds/{feed}/data')
    req.add_header('X-AIO-Key', AIO_KEY)
    req.data=f'value={value}'.encode()
    # do request
    resp = urlopen(req, timeout=4.0)
    # request status
    if resp.status == 200:
        js_str = resp.read().decode()
        print(f'data write ok (json data: {js_str})')
    else:
        print(f'unable to write data')
except urllib.error.URLError as e:
    print(f'urllib error occur: {e!r}')
