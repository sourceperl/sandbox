#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dateutil.parser
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

rte_raw_d = requests.get('https://opendata.reseaux-energies.fr/api/records/1.0/search/'
                         '?dataset=eco2mix-national-tr&rows=96&sort=-date'
                         '&facet=date_heure&refine.date_heure=%s' % time.strftime('%Y-%m-%d')).json()

rte_df = pd.DataFrame([], columns=['conso', 'eolien', 'solaire', 'hydraulique'])

for record in rte_raw_d['records']:
    if 'fields' in record:
        # extract vars
        f = record['fields']
        dt = dateutil.parser.parse(f.get('date_heure'))
        conso = float(f.get('consommation', 'nan'))
        eolien = float(f.get('eolien', 'nan'))
        solaire = float(f.get('solaire', 'nan'))
        hydraulique = float(f.get('hydraulique_step_turbinage', 'nan')) + \
                      float(f.get('hydraulique_lacs', 'nan')) + \
                      float(f.get('hydraulique_fil_eau_eclusee', 'nan'))
        # add to dataframe
        rte_df.loc[dt] = dict(conso=conso,
                              eolien=eolien,
                              solaire=solaire,
                              hydraulique=hydraulique)

rte_df['renouvelable'] = rte_df['eolien'] + rte_df['solaire'] + rte_df['hydraulique']
# rte_df['taux_couverture'] = round(100 * rte_df['renouvelable'] / rte_df['conso'], 2)

rte_df.sort_index(inplace=True)

print(rte_df.to_string())

rte_df.plot()
plt.show()
