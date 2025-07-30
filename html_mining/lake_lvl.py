#!/usr/bin/env python3

"""Parse www.smadesep.com website for extract "Serre-Ponçon" current lake level."""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup


# some class
@dataclass
class LakeInfo:
    """Lake level struct."""
    m_ngf: Optional[float] = None
    m_rel: Optional[float] = None
    obs_dt: Optional[datetime] = None


# some vars
lake_info = LakeInfo()

# HTTP request
request = Request(url='https://www.smadesep.com/lac-direct', headers={'User-Agent': ''})
uo_ret = urlopen(request, timeout=10.0)
# decode HTML syntax
soup = BeautifulSoup(uo_ret, 'html.parser')
# extract data div tag
main_div_tag = soup.find('div', attrs={'class': 'block-cote-du-lac-full'})
if not main_div_tag:
    raise RuntimeError('unable to find main div in html')
# extract date and time of current measure
d3_update_dt_tag = main_div_tag.find('h3', attrs={'class': 'title'})
if not d3_update_dt_tag:
    raise RuntimeError('unable to find h3 with update info')
# measure update date/time
date_match = re.search(r'(\d{2}/\d{2}/\d{4})', d3_update_dt_tag.text)
time_match = re.search(r'(\d{2}:\d{2})', d3_update_dt_tag.text)
if not (date_match and time_match):
    raise RuntimeError('unable to decode date and time of the measurement')
day, month, year = map(int, date_match.group().split('/'))
hour, minute = map(int, time_match.group().split(':'))
lake_info.obs_dt = datetime(year, month, day, hour, minute, tzinfo=ZoneInfo('Europe/Paris'))
# extract NGF level and below level
div_level_tag = main_div_tag.find('div', attrs={'class': 'cote-du-lac'})
if not div_level_tag:
    raise RuntimeError('unable to find level info div')
find_numbers = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', div_level_tag.text)
lake_info.m_ngf = float(find_numbers[0])
lake_info.m_rel = lake_info.m_ngf - 780
# display results (convert obs_dt: UTC to local time zone)
print(f'level NGF   : {lake_info.m_ngf:>6.02f} m')
print(f'level rel.  : {lake_info.m_rel:>6.02f} m')
print(f'level       : {90 + lake_info.m_rel:>6.02f} m')
print(f'observation : {lake_info.obs_dt.astimezone()}')
