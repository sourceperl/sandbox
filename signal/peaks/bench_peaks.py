"""
Peak Detection Comparison on a Frequency-Modulated (Chirp) Signal.

This script generates a sine wave with linearly increasing frequency (chirp),
injects Gaussian white noise, and visualizes how different SciPy 'find_peaks' 
parameters—distance, prominence, width, and threshold—perform in identifying 
local maxima within noisy data.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# build signal from 0 Hz to 50 Hz
t = np.linspace(0.0, 1.0, 1_000)
f = 50.0 * t
x = np.sin(2*np.pi*f*t)
# add gaussian noise
x += 0.15 * np.random.standard_normal(size=x.shape)

# show results
fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
fig.suptitle("SciPy find_peaks: comparison of filtering parameters", fontsize=16)


# Helper function to reduce repetitive code
def plot_peak_config(ax, peaks: list, title: str, color: str, marker: str):
    ax.plot(t, x, color='gray', alpha=0.5, label='Noisy Signal')
    ax.plot(t[peaks], x[peaks], marker, color=color, label=f'Peaks (n={len(peaks)})')
    ax.set_title(title, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize='small')


# Subplot 1: Distance (Minimum horizontal spacing)
peaks_dist, _ = find_peaks(x, distance=25)
plot_peak_config(axs[0, 0], peaks_dist, 'Parameter: distance=25', 'red', 'x')

# Subplot 2: Threshold (Vertical distance to immediate neighbors)
# very sensitive to local noise
peaks_th, _ = find_peaks(x, threshold=0.3)
plot_peak_config(axs[0, 1], peaks_th, 'Parameter: threshold=0.3', 'black', 's')

# Subplot 3: Width (Minimum width of the peak at a certain height)
peaks_wd, _ = find_peaks(x, width=5)
plot_peak_config(axs[1, 0], peaks_wd, 'Parameter: width=5', 'green', 'v')

# Subplot 4: Prominence (Vertical "standout" relative to neighbors)
# usually the most robust parameter for noisy data
peaks_prom, _ = find_peaks(x, prominence=0.8)
plot_peak_config(axs[1, 1], peaks_prom, 'Parameter: prominence=0.8', 'blue', 'o')

plt.tight_layout()
plt.show()
