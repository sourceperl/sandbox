#!/usr/bin/env python3

"""Ask for the next departure from an Ilevia bus or tram stop."""

from dataclasses import dataclass
from datetime import datetime
import json
from typing import List
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
from zoneinfo import ZoneInfo


# some const
TZ_PARIS = ZoneInfo('Europe/Paris')
BASE_URL = 'https://data.lillemetropole.fr/data/ogcapi/collections/prochains_passages/items?'


# some class
@dataclass
class Departure:
    line_code: str
    line_direction: str
    station_id: str
    station_name: str
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
    filter_str = "\"identifiant_station\" IN " \
                 "('ILEVIA:StopPoint:BP:PAS002:LOC',"\
                 " 'ILEVIA:StopPoint:BP:PAS003:LOC')"
    search_args = {'filter-lang': 'ecql-text',
                   'filter': filter_str,
                   'sortby': 'heure_estimee_depart',
                   'limit': '-1'}
    url = BASE_URL + urlencode(search_args)
    response = urlopen(url, timeout=4.0)
    # check HTTP response code
    if response.status != 200:
        raise ValueError('unable to get data from HTTP server')
    # convert response
    js_d = json.loads(response.read())
    deps_list: List[Departure] = list()
    for feature in js_d['features']:
        prop = feature['properties']
        dep = Departure(line_code=prop['code_ligne'],
                        line_direction=prop['sens_ligne'],
                        station_id=prop['identifiant_station'],
                        station_name=prop['nom_station'],
                        start_at_dt=datetime.fromisoformat(prop['heure_estimee_depart']),
                        update_at_dt=datetime.fromisoformat(prop['date_modification']))
        # alter bad timezone setting (this is a server-side bug: iso strings are marked as UTC instead of local)
        dep.start_at_dt = dep.start_at_dt.replace(tzinfo=TZ_PARIS)
        dep.update_at_dt = dep.update_at_dt.replace(tzinfo=TZ_PARIS)
        # add to list of departure
        deps_list.append(dep)
    # show results
    for dep in deps_list:
        msg = f"{dep.start_at_dt.strftime('%H:%M:%S'):8} [{dep.start_in_mn:4} mn]   {dep.line_code:6} " \
              f"{dep.station_name} -> {dep.line_direction:32}"
        print(msg)
except (KeyError, ValueError, URLError) as e:
    print(f'error occur: {e!r}')
