#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import mwclient
import pandas as pd
from difflib import SequenceMatcher

# some const
SITE_TEMPLATE = """[[Fichier:Logo GRTgaz.png|vignette|upright=1.0|Vue du site]]
{{Clear}}
 
==Données==
 
==='''[[Exploitant]]'''===
* [[Secteur de %s]]
 
==='''Coordonnées géographique'''===
* {{Position|lat=%s|lon=%s}}
* Adresse: {{Adresse|%s}}
 
==='''[[GMAO]]'''===
* {{GMAO|%s}}
 
==='''[[PCE]]'''===
* {{PCE|%s}}
 
==Accès==

''À compléter.''
 
==Sécurité==
 
''À compléter.''
 
[[Catégorie:Poste]]
[[Catégorie:%s]]"""

EXPL_LIST = ['Abbeville', 'Avion', 'Boulogne', 'Béthune', 'Carvin', 'Charleville',
             'Gauchy', 'Maubeuge', 'Reims', 'Saint-Omer']


# some functions
def is_same_str(a, b, cutoff=0.8):
    a = a.strip().upper()
    b = b.strip().upper()
    return SequenceMatcher(None, a, b).ratio() > cutoff


def best_str_in_list(test_str, str_list, cutoff=0.8):
    for s in str_list:
        if is_same_str(test_str, s, cutoff=cutoff):
            return s
    return None


# update wiki page
site = mwclient.Site(("http", "localhost:8080"), path="/")
site.login('robot', 'password')

# read data from Excel file
df = pd.read_excel('private_postes.xlsx', sheetname='Feuil1')

for index, row in df.iterrows():
    # "Poste" : "INDUS" or "DP"
    poste_type = str(row['Poste'])

    # create page
    if type(row['LIBELLE']) is str:
        # format page name
        page_name = row['LIBELLE'].strip()
        page_name = re.sub(' DP$', '', page_name, flags=re.IGNORECASE)
        page_name = re.sub(' CI$', '', page_name, flags=re.IGNORECASE)
        page_category = 'N_A'
        # add suffix and set category
        if is_same_str(poste_type, 'INDUS'):
            page_name += ' CI'
            page_category = 'CI'
        elif is_same_str(poste_type, 'DP'):
            page_name += ' DP'
            page_category = 'DP'

        # link to page_name
        p = site.Pages[page_name]

        # format all params
        exploitant = best_str_in_list(row['Exploitant'], EXPL_LIST)
        try:
            lat, lon = re.findall('\d+\.\d+', row['Coordonnée GPS'])
        except:
            lat, lon = '0.0', '0.0'
        adresse = row['Adresse site']
        code_gmao = row['Code GMAO']
        code_pce = row['Code PCE']

        page_content = SITE_TEMPLATE % (exploitant, lat, lon, adresse, code_gmao, code_pce, page_category)

        # if not p.exists:
        # if not p.text():
        if p.text() != page_content:
            print("update page: %s" % page_name)
            p.save(page_content, summary="automatic create")
            # avoid to trig update API rate limit
            time.sleep(2.0)
        else:
            print("skip page: %s" % page_name)

        # print(poste_type, row['Ville'], row['LIBELLE'], row['Exploitant'], row['Coordonnée GPS'],
        #       row['Adresse site'], row['Code GMAO'], row['Code PCE'])

# for name in ['page_1', 'page_2']:
#     page = site.Pages[name]
#     page.save('', summary="automatic create")
