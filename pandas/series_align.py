#!/usr/bin/env python3

"""
This script demonstrates how to align irregular time series data onto a fixed grid.

It uses `pd.merge_asof` with `direction='backward'` to map each fixed interval to the 
most recent known value. This is particularly useful for sensor data processing 
where samples are not perfectly aligned with wall-clock minutes or hours.
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

# perform an as-of merge to snap irregular data to the hourly grid
# 'backward' looks for the last available value occurring before or at the index time
df = pd.merge_asof(
    df.sort_index(),
    sensor_1.sort_index(),
    left_index=True,
    right_index=True,
    direction='backward'
)

# display the resulting 24-hour snapshot
with pd.option_context('display.max_rows', 50):
    print(df)
