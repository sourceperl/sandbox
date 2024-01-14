#!/usr/bin/env python3

# pandas example with CSV data from atmospheric CO2 concentrations (ppm) at Mauna Loa, Observatory, Hawaii
# display current value with matplotlib
# try to predict future values with 2nd order polynomial coefficients auto-adjust
# test with numpy==1.16.2, pandas==0.19.2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV_URL = 'https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/monthly/monthly_in_situ_co2_mlo.csv'

# read CSV as a dataframe (data from Scripps institute)
co2_month_df = pd.read_csv(CSV_URL, header=65)

# csv use -99.99 for no data: here we replace this with nan value
co2_month_df.replace(to_replace=-99.99, value=np.nan, inplace=True)

# fix column names
cols = ['year', 'month', '--', '--', 'CO2', 'seasonaly_adjusted', 'fit',
        'seasonally_adjusted_fit', 'CO2_filled', 'seasonally_adjusted_filled', 'sta']
co2_month_df.columns = cols
# remove unused columns from dataframe
cols.remove('--')
cols.remove('--')
co2_month_df = co2_month_df[cols]

# fix index to use datetime
co2_month_df['day'] = 15
co2_month_df.index = pd.to_datetime(co2_month_df[['year', 'month', 'day']])
# remove unused columns from dataframe
cols.remove('year')
cols.remove('month')
co2_month_df = co2_month_df[cols]

# format data (convert monthly data to yearly mean value)
co2_ppm = co2_month_df['CO2'].groupby([co2_month_df.index.year]).mean()
years_l = co2_ppm.index.tolist()

# init a 2nd order polynomial (here numpy use least squares to fit polynomial)
co2_poly = np.poly1d(np.polyfit(np.float64(years_l), np.float64(co2_ppm.values.tolist()), 2))

# add future years to year_list
for f_year in range(2000, 2060):
    if f_year not in years_l:
        years_l.append(f_year)

# plot data (polynomial computed and time series from csv)
plt.plot(years_l, co2_poly(np.float64(years_l)), 'r--')
co2_ppm.plot(style='b')

plt.title('Atmospheric CO2 concentrations at Mauna Loa, Observatory, Hawaii')
plt.xlabel('years')
plt.ylabel('CO2 concentrations (ppm)')
plt.grid()
plt.show()
