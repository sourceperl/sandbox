""" Convert a VictoriaMetrics json query result (Prometheus format) to a pandas TimeSeries and then to a CSV. """

import json
from pathlib import Path

import pandas as pd

# load data from VictoriaMetrics json file
script_dir = Path(__file__).parent
file_path = script_dir / 'data' / 'export.json'

with open(file_path, 'r') as f:
    raw_data = json.load(f)

# extract the values (list of [timestamp, value])
data_list = raw_data['data']['result'][0]['values']

# convert to pandas DataFrame with a DatetimeIndex (UTC)
df = pd.DataFrame(data_list, columns=['timestamp', 'value'])
df['timestamp'] = pd.to_datetime(df['timestamp'].astype(float), unit='s', utc=True)
df['value'] = df['value'].astype(float).round(0)
df = df.set_index('timestamp')

# filter
start_date = pd.Timestamp('2026-04-08 06:12:00', tz='UTC')
end_date = start_date + pd.Timedelta(minutes=59)
filtered = df.loc[start_date:end_date].sort_index()

# create a complete minute-by-minute index for the full week
full_index = pd.date_range(start=start_date, end=end_date, freq='min')

# reindex to full index — missing rows become NaN
full_df = filtered.reindex(full_index)

# report gaps before interpolation
missing = full_df[full_df['value'].isna()]
print(f'expected rows: {len(full_index)}')
print(f'actual rows:   {len(filtered)}')
print(f'missing timestamps ({len(missing)}) in the original data:')
for ts in missing.index:
    print(f'  {ts}')

# interpolate missing values linearly
full_df['value'] = full_df['value'].interpolate(method='linear')
full_df['value'] = full_df['value'].round(0)

# output
full_df.to_csv(script_dir / 'output.csv', sep=';', header=False, date_format='%Y-%m-%dT%H:%M:%SZ', encoding='utf-8-sig')
