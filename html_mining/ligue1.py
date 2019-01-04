#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import requests
from bs4 import BeautifulSoup

r = requests.get("http://m.lfp.fr/ligue1/classement")

if r.status_code == 200:
    od_l1_club = OrderedDict()
    s = BeautifulSoup(r.content, "html.parser")

    # first table on page
    t = s.find_all("table")[0]

    # each row in table
    for row in t.find_all("tr"):
        name = row.find("td", attrs={"class": "club"})
        if name:
            # club name as dict key
            name = name.text.strip()
            od_l1_club[name] = OrderedDict()
            # find rank
            od_l1_club[name]['rank'] = row.find("td").text.strip()
            # find points
            od_l1_club[name]['pts'] = row.find("td", attrs={"class": "pts"}).text.strip()
            # find all stats
            l_td_center = row.find_all("td", attrs={"class": "center"})
            if l_td_center:
                od_l1_club[name]["played"] = l_td_center[0].text.strip()
                od_l1_club[name]["wins"] = l_td_center[1].text.strip()
                od_l1_club[name]["draws"] = l_td_center[2].text.strip()
                od_l1_club[name]["loses"] = l_td_center[3].text.strip()
                od_l1_club[name]["for"] = l_td_center[4].text.strip()
                od_l1_club[name]["against"] = l_td_center[5].text.strip()
                od_l1_club[name]["diff"] = l_td_center[6].text.strip()

    # display result store in od_l1_club
    l_disp_items = ["rank", "played", "wins", "draws", "loses", "for", "against", "diff", "pts"]
    # format string
    fmt = "%-24s" + " %8s" * len(l_disp_items)
    # print head
    h_str = fmt % tuple(["club"] + l_disp_items)
    print(h_str)
    print("-" * len(h_str))
    # print all rows
    for l1_club, d_item in od_l1_club.items():
            print(fmt % tuple([l1_club] + [d_item[i] for i in l_disp_items]))
