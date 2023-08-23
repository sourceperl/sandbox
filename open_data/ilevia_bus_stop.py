#!/usr/bin/env python3

"""Ask for the next departure from an Ilevia bus stop."""

from datetime import datetime, timezone
import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


# some const
BASE_URL = 'https://opendata.lillemetropole.fr/api/explore/v2.1/catalog/datasets/ilevia-prochainspassages/records?'


# request data from MEL opendata platform
try:
    search_args = {'order_by': 'heureestimeedepart', 'refine': 'nomstation:GARE LILLE FLANDRES'}
    url = BASE_URL + urlencode(search_args)
    response = urlopen(url, timeout=4.0)
    # check HTTP response code
    if response.status != 200:
        raise ValueError('unable to get data from HTTP server')
    # convert response
    js_d = json.loads(response.read())
    for record in js_d['results']:
        line_id = record['codeligne']
        dest_id = record['sensligne']
        update_dt = datetime.fromisoformat(record['datemodification']).replace(tzinfo=timezone.utc).astimezone(tz=None)
        start_dt = datetime.fromisoformat(record['heureestimeedepart']).replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(f'{line_id:6} {dest_id:28} start at {start_dt!s}   [update {update_dt!s}]')
except (KeyError, ValueError, URLError) as e:
    print(f'error occur: {e!r}')
