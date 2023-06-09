#!/usr/bin/env python3

"""Request injection of biomethane into the GRTgaz network history from ODRE platform."""

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
    search_args = {'dataset': 'prod-nat-gaz-horaire-prov', 'sort': 'journee_gaziere', 'rows': '7',
                   'refine.operateur': 'GRTgaz', }
    url = SEARCH_URL + urlencode(search_args)
    resp = urlopen(url, timeout=4.0)
    # convert response to an items list [(year, month, igra), (year, month+1, igra), ...]
    resp_d = json.loads(resp.read())
    items_l = []
    for record in resp_d['records']:
        item_year, item_month, item_day = map(str, record['fields']['journee_gaziere'].split('-')[:3])
        item_prod = float(record['fields']['prod_journaliere_mwh_pcs'])
        items_l.append((item_year, item_month, item_day, item_prod))
    # convert items list for plot
    x, heights = [], []
    for year, month, day, prod in sorted(items_l):
        x.append(f'{day}/{month}')
        heights.append(prod)
    # set figure size and draw bar plot
    fig, ax = plt.subplots(1, 1, figsize=FIG_SIZE, dpi=DPI)
    ax.bar(x, heights)
    # add value as labels in bars
    for i, h in enumerate(heights):
        ax.text(i, h/2, f'{h:.0f}', ha='center', bbox=dict(facecolor='white', alpha=0.5))
    # labels
    ax.set_title('Production journalière de biométhane sur le réseau de GRTgaz')
    ax.set_ylabel('Production (MWh)')
    plt.show()
except (KeyError, TypeError, URLError) as e:
    print(f'error occur: {e!r}')
