#!/usr/bin/env python3

"""
Crypto Analysis: EWMA Sensitivity Study.

This script compares different alpha factors for the Exponential Weighted 
Moving Average on Bitcoin prices to visualize the lag vs. smoothing trade-off.
"""

from pathlib import Path

import matplotlib.pyplot as plt

import pandas as pd

# load data
SCRIPT_DIR = Path(__file__).parent
DATA_PATH = SCRIPT_DIR / '..' / 'datasets' / 'BTC-EUR.csv.xz'

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")

# load and slice data once to improve performance
btc_full = pd.read_csv(DATA_PATH, index_col='Date', parse_dates=True)
# "Close" column for every 2019 records
btc_2019 = btc_full['Close'].loc['2019']

# plotting
plt.figure(figsize=(12, 7))

# plot raw closing price as the solid baseline
plt.plot(btc_2019, label='BTC Close (Raw)', color='black', linestyle='--', linewidth=1.0, alpha=0.5, zorder=3)

# manual color configuration
# using a high-contrast palette: Blue, Orange, Green, Red
colors = ['#3498DB', '#E67E22', '#2ECC71', '#E74C3C']
alphas = [0.2, 0.4, 0.6, 0.8]

for alpha, color in zip(alphas, colors):
    ewma_series = btc_2019.ewm(alpha=alpha, adjust=False).mean()
    plt.plot(ewma_series,
             label=f'α = {alpha}',
             # linestyle='--',
             alpha=0.9,
             color=color)

# refine Chart
plt.title('Bitcoin (BTC-EUR) - 2019: EWMA Alpha Comparison', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Price (EUR)')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(title='Smoothing Factor (Alpha)', loc='best')

# clean up date formatting on X-axis
plt.gcf().autofmt_xdate()
plt.tight_layout()

plt.show()
