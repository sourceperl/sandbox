#!/usr/bin/env python3

"""Basic influxdb insert with an HTTP POST request."""

import time
import urllib.error
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# format URL for write data
write_opts = urlencode(dict(bucket='mydb', precision='s'))
url = f'http://192.168.0.22:8086/api/v2/write?{write_opts}'

# POST payload
value = 42.0
timestamp = round(time.time())
data = f'test_sensors,sensor=foo,location=nowhere value={value} {timestamp}'.encode()

# POST data to influxdb
print(f'POST: {data} at: {url}')
try:
    # do request
    urlopen(Request(url, data=data), timeout=4.0)
    # print status
    print('write ok')
except urllib.error.URLError as e:
    print(f'error occur: {e!r}')
