#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# some const
QUALITY_LVL = ("n/a", "très bon", "très bon", "bon", "bon", "moyen",
               "médiocre", "médiocre", "mauvais", "mauvais", "très mauvais")


# some class
class AtmoHdfBeautifulSoup(BeautifulSoup):
    def find_ville_id(self, ville_id):
        try:
            str_ssindice = '{"indice": "france", "periode": "ajd", "ville_id": "%i"}' % ville_id
            lvl = int(self.find("div", attrs={"data-ssindice": str_ssindice}).find("span").text.strip())
        except (AttributeError, ValueError):
            lvl = 0
        return lvl, QUALITY_LVL[lvl]


# do requests
r = requests.get("http://www.atmo-hdf.fr/")

if r.status_code == 200:
    air_quality_index = {}
    bs = AtmoHdfBeautifulSoup(r.content, "html.parser")

    # search today index for some ids
    air_quality_index["lille"] = bs.find_ville_id(13)
    air_quality_index["dunkerque"] = bs.find_ville_id(19)
    air_quality_index["valenciennes"] = bs.find_ville_id(22)
    air_quality_index["maubeuge"] = bs.find_ville_id(16)

    print(air_quality_index)
