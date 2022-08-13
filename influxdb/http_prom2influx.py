#!/usr/bin/env python3

"""Copy a prometheus metric to an influxdb measurement."""

import json
import urllib.error
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# some const
PERIOD='10d'
FROM_METRIC = 'web_flux'
TO_MEASURE = 'web_flux'

try:
    # request prometheus data
    print('> request prometheus data')
    prom_args = urlencode({'query':f'{FROM_METRIC}{{}}[{PERIOD}]'})
    resp = urlopen(f'http://192.168.1.60:9090/api/v1/query?{prom_args}', timeout=4.0)
    prom_data = json.loads(resp.read())
    # format influxdb txt
    print('> format data for influxdb')
    influx_txt = ''
    for (timestamp, value) in (prom_data['data']['result'][0]['values']):
        influx_txt += f'{TO_MEASURE} value={value} {timestamp}\n'
    influx_txt = influx_txt.encode()
    # send data to influxdb
    print('> send data to influxdb')
    influx_args = urlencode(dict(bucket='mydb', precision='s'))
    urlopen(Request(f'http://192.168.1.60:8086/api/v2/write?{influx_args}', data=influx_txt), timeout=4.0)
except urllib.error.URLError as e:
    print(f'error occur: {e!r}')
