#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# use python package metar from https://github.com/python-metar/python-metar

from metar import Metar
import requests

r = requests.get("http://tgftp.nws.noaa.gov/data/observations/metar/stations/LFQQ.TXT")

if r.status_code == 200:
    m = r.content.decode().split("\n")[1]
    obs = Metar.Metar(m)
    print(obs.string())
