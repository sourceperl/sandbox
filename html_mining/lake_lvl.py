#!/usr/bin/env python3

"""Parse www.smadesep.com website for extract "Serre-Ponçon" current lake level."""

from datetime import datetime, timezone
from dataclasses import dataclass
import re
import requests
from bs4 import BeautifulSoup


# some class
@dataclass
class Level:
    """Lake level struct."""
    m_ngf: float = None
    m_rel: float = None
    obs_dt: datetime = None


# some vars
lvl = Level()

# HTTP request
resp = requests.get('http://www.smadesep.com/cms/index.php/la-cote-du-lac/', headers={'User-Agent': ''})

# process response
try:
    if resp.status_code != 200:
        raise ValueError('unable to retrieve web page')
    # decode HTML syntax
    soup = BeautifulSoup(resp.content, 'html.parser')
    # extract data div tag
    div_tag = soup.find('div', attrs={'class': 'lacote'})
    if not div_tag:
        raise ValueError('unable to find div tag in html')
    # extract date and time of current measure
    span_date_tag = div_tag.find('span', attrs={'class': 'the_date'})
    if not span_date_tag:
        raise ValueError('unable to find "date" span tag in div tag')
    # decode date and time
    date_match = re.search(r'(\d{2}-\d{2}-\d{4})', span_date_tag.text)
    time_match = re.search(r'(\d{2}:\d{2})', span_date_tag.text)
    if date_match and time_match:
        day, month, year = map(int, date_match.group().split('-'))
        hour, minute = map(int, time_match.group().split(':'))
        lvl.obs_dt = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
    # extract NGF level and below level
    span_level_tag = div_tag.find('span', attrs={'class': 'the_lacote'})
    if not span_level_tag:
        raise ValueError('unable to find "cote" span tag in div tag')
    find_numbers = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', span_level_tag.text)
    lvl.m_ngf = float(find_numbers[0])
    lvl.m_rel = lvl.m_ngf - 780
    # display results (convert obs_dt: UTC to local time zone)
    print(f'level NGF   : {lvl.m_ngf:>6.02f} m')
    print(f'level rel.  : {lvl.m_rel:>6.02f} m')
    print(f'level       : {90 + lvl.m_rel:>6.02f} m')
    print(f'observation : {lvl.obs_dt.astimezone()}')
except (IndexError, ValueError) as e:
    print(e)
