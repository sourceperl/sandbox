"""
this script loads a dataset of float values from a text file and generates
a comprehensive statistical visualization. it highlights the central 80% 
of the data volume and compares the empirical distribution (kde) with a 
theoretical normal distribution (gaussian fit).
"""

import gzip
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde, norm

# load and process data
script_dir = Path(__file__).resolve().parent
data_file_path = script_dir / 'data.txt.gz'
with gzip.open(data_file_path, 'rt') as f:
    data = np.genfromtxt(f, dtype=float)
data = np.round(data, decimals=2)

# statistical calculations
x, y = np.unique(data, return_counts=True)
y_percentage = (y / len(data)) * 100
mean_val = float(np.mean(data))
std_val = float(np.std(data))

# calculate 80% volume (between 10th and 90th percentiles)
p10 = float(np.percentile(data, 10))
p90 = float(np.percentile(data, 90))

# create plot
plt.figure(figsize=(14, 8))

# plot the frequency bars
plt.bar(x, y_percentage, width=0.015, color='royalblue', alpha=0.3, label='frequency (%)', align='center')

# add the kde (smooth density curve)
kde = gaussian_kde(data, bw_method=0.4)
x_range = np.linspace(x.min(), x.max(), 1000)
# scale factor to align curves with percentage bars peak
# we use the max of the bars to ensure the scale is consistent
scale_factor = y_percentage.max()

# kde curve
kde_raw = kde(x_range)
kde_values = kde_raw * (scale_factor / kde_raw.max())
plt.plot(x_range, kde_values, color='darkblue', lw=2, label='distribution shape (kde)')

# fitted a normal gaussian curve
# calculate the theoretical normal distribution
gaussian_raw = norm.pdf(x_range, mean_val, std_val)
gaussian_values = gaussian_raw * (scale_factor / gaussian_raw.max())
plt.plot(x_range, gaussian_values, color='forestgreen', lw=2, linestyle='--', label='fitted normal (gaussian)')

# shade the central 80% region under the kde
x_80 = np.linspace(p10, p90, 500)
y_80 = kde(x_80) * (scale_factor / kde_raw.max())
plt.fill_between(x_80, y_80, color='orange', alpha=0.3, label=f'central 80% ({p10:.2f} to {p90:.2f})')

# add vertical lines for boundaries and mean
plt.axvline(p10, color='orange', linestyle=':', lw=1.5)
plt.axvline(p90, color='orange', linestyle=':', lw=1.5)
plt.axvline(mean_val, color='red', linestyle='--', lw=2, label=rf'mean: {mean_val:.2f} ($\sigma = {std_val:.2f}$)')

# formatting and labels
plt.title(f'distribution analysis with gaussian fit (n={len(data)} samples)', fontsize=14, fontweight='bold')
plt.xlabel('measured values', fontsize=12)
plt.ylabel('frequency (%)', fontsize=12)

# set xticks (using 0.02 for readability, change to 0.01 if range is small)
plt.xticks(np.arange(data.min(), data.max() + 0.001, 0.02), rotation=90, fontsize=8)

plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, shadow=True, loc='upper right')


plt.tight_layout()
plt.show()
