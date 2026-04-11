#!/usr/bin/env python3

"""
Align irregular time series data onto a fixed hourly grid.

Raw sensor samples carry sub-minute timestamps and mixed UTC offsets.

The alignment strategy is:
  1. Merge the raw timestamps into the hourly index so no sample is lost.
  2. Forward-fill to propagate each reading until the next one arrives.
  3. Reindex back to the hourly grid, discarding the intermediate ticks.

This avoids `merge_asof` overhead while correctly handling samples that
do not land exactly on hourly boundaries.
"""

import pandas as pd

# sample raw data with sub-minute precision
samples = [
    {'value':  0.5, 'dt': '2026-01-01T00:30:00Z'},
    {'value':  1.1, 'dt': '2026-01-01T01:10:10+00:00'},
    {'value':  5.3, 'dt': '2026-01-01T05:30:20Z'},
    {'value': 12.0, 'dt': '2026-01-01T14:00:00+02:00'}
]

# create the series and force utc to ensure compatibility with the master index
sensor_1 = pd.Series(
    data=[d['value'] for d in samples],
    index=pd.to_datetime([d['dt'] for d in samples], format='ISO8601', utc=True),
    name='sensor_1'
)

# remove the index name for a cleaner look
sensor_1.index.name = None

# define a master hourly index for 24 hours
df_index = pd.date_range(start='2026-01-01 00:00:00', periods=24, freq='1h', tz='UTC')
df = pd.DataFrame(index=df_index)

# for each hour of df_index, retrieve the last known value
df['sensor_1'] = sensor_1.reindex(df_index, method='ffill')

# display the resulting 24-hour snapshot
with pd.option_context('display.max_rows', 50):
    print(df)
