#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
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
%s

==='''[[PCE]]'''===
%s

==Accès==

''À compléter.''
 
==Sécurité==
 
''À compléter.''
 
[[Catégorie:Site Nord]]
[[Catégorie:%s]]"""

EXPL_LIST = ['Abbeville', 'Avion', 'Boulogne', 'Béthune', 'Carvin', 'Charleville',
             'Gauchy', 'Maubeuge', 'Reims', 'Saint-Omer', 'Valenciennes']


# some functions
def is_same_str(a, b, cutoff=0.8):
    a = a.strip().upper()
    b = b.strip().upper()
    return SequenceMatcher(None, a, b).ratio() > cutoff


def best_str_in_list(test_str, str_list, cutoff=0.8):
    for s in str_list:
        if is_same_str(test_str, s, cutoff=cutoff):
            return s
    return ''


# update wiki page
site = mwclient.Site(("http", "localhost:8080"), path="/")
site.login('robot', 'password')

# read data from Excel file (replace null value by '')
df = pd.read_excel('private_postes.xlsx', sheetname='Feuil1')
df.fillna('', inplace=True)

for index, row in df.iterrows():
    # "Poste" : "INDUS" or "DP"
    poste_type = str(row['Type'])

    # create page
    if type(row['Libellé']) is str:
        # format page name
        page_name = row['Libellé'].strip()
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
        elif is_same_str(poste_type, 'SEC'):
            page_name += ' SEC'
            page_category = 'SEC'
        elif is_same_str(poste_type, 'SEC'):
            page_name += ' PRED'
            page_category = 'PRED'
        elif is_same_str(poste_type, 'STA'):
            page_name += ''
            page_category = ''

        # link to page_name
        p = site.Pages[page_name]

        # format all params
        # exploitant
        exploitant = best_str_in_list(row['Exploitant'], EXPL_LIST)

        # gps coord
        try:
            lat = '%.6f' % float(row['gps_lat'])
            lon = '%.6f' % float(row['gps_lon'])
        except:
            print("error: unable to decode GPS lat and/or lon value(s) for page \"%s\"" % page_name, file=sys.stderr)
            lat = '0.0'
            lon = '0.0'

        # postal address
        adresse = str(row['Adresse'])

        # GMAO code
        code_gmao = ''
        try:
            # for each code in string "code1, code2, ..."
            for code in (map(str.strip, str(row['Code GMAO']).split(','))):
                # no null string code add a GMAO template
                if code.strip():
                    code_gmao += '\n* {{GMAO|%s}}' % code
        except:
            print("error: unable to decode GMAO code(s) for page \"%s\"" % page_name, file=sys.stderr)
            code_gmao = ''

        # PCE code
        code_pce = ''
        try:
            # for each code in string "code1, code2, ..."
            for code in (map(str.strip, str(row['Code PCE']).split(','))):
                # no null string code add a PCE template
                if code.strip():
                    code_pce += '\n* {{PCE|%s}}' % code
        except:
            print("error: unable to decode PCE code(s) for page \"%s\"" % page_name, file=sys.stderr)
            code_pce = ''

        # format page
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
