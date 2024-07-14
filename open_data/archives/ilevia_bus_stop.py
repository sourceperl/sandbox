#!/usr/bin/env python3

"""Ask for the next departure from an Ilevia bus or tram stop."""

from dataclasses import dataclass
from datetime import datetime
import json
from typing import List
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


# some const
BASE_URL = 'https://opendata.lillemetropole.fr/api/explore/v2.1/catalog/datasets/ilevia-prochainspassages/records?'


# some class
@dataclass
class Departure:
    line_id: str
    dest_id: str
    station_id: str
    start_at_dt: datetime
    update_at_dt: datetime

    @property
    def start_in_mn(self) -> float:
        now_dt = datetime.now().astimezone(tz=None)
        if self.start_at_dt > now_dt:
            return round((self.start_at_dt - now_dt).seconds / 60, 1)
        else:
            return 0.0


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
    deps_list: List[Departure] = list()
    for record in js_d['results']:
        dep = Departure(line_id=record['codeligne'],
                        dest_id=record['sensligne'],
                        station_id=record['identifiantstation'],
                        start_at_dt=datetime.fromisoformat(record['heureestimeedepart']).astimezone(tz=None),
                        update_at_dt=datetime.fromisoformat(record['datemodification']).astimezone(tz=None))
        deps_list.append(dep)
    # show results
    for dep in deps_list:
        msg = f"{dep.start_at_dt.strftime('%H:%M:%S'):8} [{dep.start_in_mn:4} mn]   {dep.line_id:6} {dep.dest_id:32}"
        print(msg)
except (KeyError, ValueError, URLError) as e:
    print(f'error occur: {e!r}')
