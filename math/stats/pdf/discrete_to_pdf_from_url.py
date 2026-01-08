"""
Kernel Density Estimation (KDE) Visualization for Time Series Data

This script downloads and analyzes time series data using kernel density estimation.
It generates two visualizations:
1. Raw time series data plot
2. Probability density function (PDF) with KDE analysis

The KDE visualization shows:
- The estimated probability density function
- The most frequent value in the dataset
- The PDF peak location
- Statistical metrics (bandwidth, integral, peak offset)
"""

import lzma
from io import BytesIO
from urllib.request import urlopen

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

data_url = 'https://github.com/sourceperl/datasets/raw/995033b1993dfddc12f6f3626e7a9b7181b6dd68/ts/mine-ts-1.txt.xz'

with urlopen(data_url) as response:
    compressed_data = response.read()
    with lzma.open(BytesIO(compressed_data), 'rt') as f:
        data = np.genfromtxt(f, dtype=float)
# remove nan values
data = data[~np.isnan(data)]

# define plotting range with margins to capture distribution tails
margin = data.std()
x_range = np.linspace(data.min() - margin, data.max() + margin, 1000)

# kernel density estimation
kde = gaussian_kde(data, bw_method=0.25)

# calculate probability density function
pdf = kde(x_range)

# calculate statistics
bandwidth = kde.factor * data.std()
unique_vals, counts = np.unique(data, return_counts=True)
most_frequent_val = unique_vals[np.argmax(counts)]
most_frequent_count = np.max(counts)
pdf_peak_location = x_range[np.argmax(pdf)]
pdf_integral = np.trapezoid(pdf, x_range)

# plot 1: raw series data
plt.subplot(211)
plt.plot(data)
plt.title('RAW data', fontsize=13, fontweight='bold', pad=15)
plt.grid(True, linestyle=':', alpha=0.6)

# plot 2: individual gaussians and their sum
# plot the combined kde
plt.subplot(212)
plt.plot(x_range, pdf, color='red', linewidth=2.5, label='total kde', zorder=5)
# highlight the most frequent value
plt.axvline(most_frequent_val, color='blue', linestyle='--', linewidth=2,
            label=f'most frequent: x={most_frequent_val} ({most_frequent_count}×)', zorder=2)
# highlight the pdf peak
plt.axvline(pdf_peak_location, color='green', linestyle='--', linewidth=2,
            label=f'pdf peak: x={pdf_peak_location:.2f}', zorder=2)
# mark the peak with a dot
plt.plot(pdf_peak_location, np.max(pdf), 'go', markersize=8, zorder=6)
# add statistics annotation
stats_text = (f'bandwidth: {bandwidth:.3f}\n'
              f'integral: {pdf_integral:.4f}\n'
              f'peak offset: {abs(pdf_peak_location - most_frequent_val):.2f}')
bbox_d = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
plt.text(0.02, 0.97, stats_text, transform=plt.gca().transAxes, fontsize=9,
         verticalalignment='top', horizontalalignment='left', bbox=bbox_d)
plt.title('individual gaussian kernels', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('value', fontsize=11)
plt.ylabel('density', fontsize=11)
plt.legend(fontsize=10, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()
