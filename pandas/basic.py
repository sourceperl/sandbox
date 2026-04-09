#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

# create some Series with a DatetimeIndex
dates = pd.date_range(start='2026-01-01', end='2026-12-31', freq='D')
series_1 = pd.Series(np.random.randn(len(dates)).cumsum(), index=dates)
series_2 = pd.Series(np.random.randn(len(dates)).cumsum(), index=dates)
series_3 = series_1 + series_2

# plot from the Series object
series_1.plot(kind='line', figsize=(10, 5), color='teal', linewidth=2, label='series 1')
series_2.plot(kind='line', figsize=(10, 5), color='salmon', linewidth=2, label='series 2')
series_3.plot(kind='line', figsize=(10, 5), color='royalblue', linewidth=2, linestyle=':', label='add series (1+2)')

# customize plot
plt.title("Time Series Analysis (pd.Series)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylabel("Cumulative Value")
plt.legend(loc='best')
plt.show()
