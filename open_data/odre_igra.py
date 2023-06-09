#!/usr/bin/env python3

"""Request IGRa indicator history from ODRE platform."""

import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
import matplotlib.pyplot as plt


# some const
SEARCH_URL = 'https://odre.opendatasoft.com/api/records/1.0/search/?'
DPI = 96
FIG_SIZE = (546/DPI, 227/DPI)


try:
    # request
    search_args = {'dataset': 'igra-reg', 'sort': 'date', 'rows': '12',
                   'refine.nom_officiel_region': 'Hauts-de-France', }
    url = SEARCH_URL + urlencode(search_args)
    resp = urlopen(url, timeout=4.0)
    # convert response to an items list [(year, month, igra), (year, month+1, igra), ...]
    resp_d = json.loads(resp.read())
    items_l = []
    for record in resp_d['records']:
        item_year, item_month = map(str, record['fields']['date'].split('-')[:2])
        item_igra = float(record['fields']['igra'])
        items_l.append((item_year, item_month, item_igra))
    # convert items list for plot
    x, heights = [], []
    for year, month, igra in sorted(items_l):
        x.append(f'{month}')
        heights.append(igra)
    # set figure size and draw bar plot
    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.bar(x, heights)
    # add value as labels in bars
    for i, h in enumerate(heights):
        plt.text(i, h/2, f'{h:.01f}', ha='center', bbox=dict(facecolor='white', alpha=0.5))
    # title
    plt.title('Indicateur annualisé gaz renouvelable dans les Hauts-de-France')
    # axes labels
    plt.ylabel('IGRa (%)')
    plt.show()
except (KeyError, TypeError, URLError) as e:
    print(f'error occur: {e!r}')
