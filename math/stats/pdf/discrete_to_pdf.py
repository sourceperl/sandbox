"""
kernel density estimation (kde) visualization

this script demonstrates how kernel density estimation works by visualizing:
1. individual gaussian kernels placed at each data point
2. the resulting probability density function (pdf) as the sum of all kernels

the visualization helps understand why kde peaks may not align exactly with
the most frequent data values, as the pdf results from overlapping gaussians.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from scipy.stats import gaussian_kde, norm

# sample data
data = np.array([1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9, 10, 11, 12])


# define plotting range with margins to capture distribution tails
margin = data.std()
x_range = np.linspace(data.min() - margin, data.max() + margin, 1000)

# kernel density estimation
kde = gaussian_kde(data, bw_method=0.3)

# calculate probability density function
pdf = kde(x_range)

# calculate statistics
bandwidth = kde.factor * data.std()
unique_vals, counts = np.unique(data, return_counts=True)
most_frequent_val = unique_vals[np.argmax(counts)]
most_frequent_count = np.max(counts)
pdf_peak_location = x_range[np.argmax(pdf)]
pdf_integral = np.trapezoid(pdf, x_range)

# create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))

# plot 1: individual gaussians and their sum
# plot individual gaussian kernels with height reflecting frequency
unique_points, point_counts = np.unique(data, return_counts=True)
for point, count in zip(unique_points, point_counts):
    individual_gaussian = norm.pdf(x_range, point, bandwidth) * count / len(data)
    ax1.plot(x_range, individual_gaussian, alpha=0.3, linewidth=1, color='steelblue')
    ax1.axvline(point, color='gray', linestyle=':', alpha=0.4, linewidth=0.8)

# plot the combined kde
ax1.plot(x_range, pdf, color='red', linewidth=2.5, label='total kde (sum of kernels)', zorder=5)
ax1.set_title('individual gaussian kernels and their sum', fontsize=13, fontweight='bold', pad=15)
ax1.set_xlabel('value', fontsize=11)
ax1.set_ylabel('density', fontsize=11)
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.xaxis.set_major_locator(MultipleLocator(1))

# plot 2: final pdf with data points and annotations
# plot pdf
ax2.plot(x_range, pdf, color='red', linewidth=2.5, label='estimated pdf', zorder=3)
ax2.fill_between(x_range, pdf, alpha=0.3, color='red')

# highlight the most frequent value
ax2.axvline(most_frequent_val, color='blue', linestyle='--', linewidth=2,
            label=f'most frequent: x={most_frequent_val} ({most_frequent_count}×)', zorder=2)

# highlight the pdf peak
ax2.axvline(pdf_peak_location, color='green', linestyle='--', linewidth=2,
            label=f'pdf peak: x={pdf_peak_location:.2f}', zorder=2)

# add rug plot to show individual data points
ax2.scatter(data, np.zeros_like(data), color='black', alpha=0.6, s=50,
            marker='|', linewidths=2, label='data points', zorder=5)

# mark the peak with a dot
ax2.plot(pdf_peak_location, np.max(pdf), 'go', markersize=8, zorder=6)

ax2.set_title('final probability density function', fontsize=13, fontweight='bold', pad=15)
ax2.set_xlabel('value', fontsize=11)
ax2.set_ylabel('density', fontsize=11)
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.xaxis.set_major_locator(MultipleLocator(1))
ax2.set_ylim(bottom=-0.01)

# add statistics annotation
stats_text = (f'bandwidth: {bandwidth:.3f}\n'
              f'integral: {pdf_integral:.4f}\n'
              f'peak offset: {abs(pdf_peak_location - most_frequent_val):.2f}')
ax2.text(0.02, 0.97, stats_text, transform=ax2.transAxes,
         fontsize=9, verticalalignment='top', horizontalalignment='left',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

plt.tight_layout()
plt.show()

# print summary statistics
print(f"\ndata summary:")
print(f"  sample size: {len(data)}")
print(f"  mean: {data.mean():.2f}")
print(f"  std dev: {data.std():.2f}")
print(f"\nkde parameters:")
print(f"  bandwidth: {bandwidth:.3f}")
print(f"  pdf integral: {pdf_integral:.4f}")
print(f"\ncomparison:")
print(f"  most frequent value: {most_frequent_val} (appears {most_frequent_count}×)")
print(f"  pdf peak location: {pdf_peak_location:.2f}")
print(f"  peak offset: {abs(pdf_peak_location - most_frequent_val):.2f}")
