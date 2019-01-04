#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

r = requests.get("https://twitter.com/ThePSF", headers={"User-Agent": ""})

if r.status_code == 200:
    s = BeautifulSoup(r.content, "html.parser")
    # extract tweets
    l_tw = []
    for p in s.find_all("p", attrs={"class": "tweet-text"}):
        l_tw.append(p.text.strip())

    print(l_tw)
