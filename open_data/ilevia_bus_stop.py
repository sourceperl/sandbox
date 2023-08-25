#!/usr/bin/env python3

"""Ask for the next departure from an Ilevia bus stop."""

from datetime import datetime
import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


# some const
BASE_URL = 'https://opendata.lillemetropole.fr/api/explore/v2.1/catalog/datasets/ilevia-prochainspassages/records?'


# request data from MEL opendata platform
try:
    search_args = {'order_by': 'heureestimeedepart', 'refine': 'nomstation:REPUBLIQUE BEAUX ARTS', 'limit': '100'}
    url = BASE_URL + urlencode(search_args)
    response = urlopen(url, timeout=4.0)
    # check HTTP response code
    if response.status != 200:
        raise ValueError('unable to get data from HTTP server')
    # convert response
    js_d = json.loads(response.read())
    deps_l = []
    for record in js_d['results']:
        line_id = record['codeligne']
        dest_id = record['sensligne']
        station_id = record['identifiantstation']
        start_dt = datetime.fromisoformat(record['heureestimeedepart']).astimezone(tz=None)
        update_dt = datetime.fromisoformat(record['datemodification']).astimezone(tz=None)
        deps_l.append(dict(line_id=line_id, dest_id=dest_id, station_id=station_id,
                           start_dt=start_dt, update_dt=update_dt))
    # show results
    for dep_d in deps_l:
        msg = (f"{dep_d['start_dt'].strftime('%H:%M:%S'):10}"
               f"{dep_d['line_id']:6} {dep_d['dest_id']:32}")
        print(msg)
except (KeyError, ValueError, URLError) as e:
    print(f'error occur: {e!r}')
