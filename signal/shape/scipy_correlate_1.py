"""
Calculates the time shift (lag) and similarity between two time series (S1 and S2) using normalized Cross-Correlation.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import correlate, correlation_lags

# 1 sample/minute, shift 10 samples (= 10 minutes)
sample_time = 1
expected_shift_samples = 10

# build signals 1 and 2
script_dir = Path(__file__).resolve().parent
data_file_path = script_dir / 'datasets/raw_data.txt'
# load RAW signal from txt file
s1 = np.genfromtxt(data_file_path, dtype=float)
s2 = np.roll(s1, expected_shift_samples)
s2[:expected_shift_samples] = np.mean(s1[:expected_shift_samples])

# center the signals (remove the mean)
s1_centered = s1 - np.mean(s1)
s2_centered = s2 - np.mean(s2)

# calculate the raw cross-correlation
correlation_raw = correlate(s1_centered, s2_centered, mode='full', method='auto')

# normalization (correlation coefficient between -1 and 1)
# using the energy/variance of the centered signals (product of the total variance/energy of the entire signals)
variance_s1 = np.sum(s1_centered**2)
variance_s2 = np.sum(s2_centered**2)

# calculate the normalized correlation function
correlation_normalized = correlation_raw / np.sqrt(variance_s1 * variance_s2)

# calculate the corresponding lags (in samples)
lags_samples = correlation_lags(s1.size, s2.size, mode='full')

# the shift in samples and minutes
max_index = np.argmax(correlation_normalized)
shift_samples = lags_samples[max_index]
shift_minutes = shift_samples * sample_time

# value of the coefficient at the maximum (similarity measure)
similarity = correlation_normalized[max_index]

# visualization of results
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=False)

print(f"--- Time Series Analysis Results ---")
print(f"expected shift for reporting (minutes): {expected_shift_samples * sample_time} minutes")
print(f"found shift (samples): {shift_samples}")
print(f"found shift (minutes): {shift_minutes} minutes")
print(f"maximum similarity (correlation coefficient): {similarity:.3f}")

# plot 1: Original Signals
ax1.plot(s1, label='Signal S1', alpha=0.7)
ax1.plot(s2, label='Signal S2', alpha=0.7)
ax1.set_title('Original Signals')
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Amplitude')
ax1.legend()
ax1.grid()

# plot 2: Normalized Cross-Correlation Function
lags_minutes = lags_samples * sample_time

ax2.plot(lags_minutes, correlation_normalized)
ax2.axvline(shift_minutes, color='r', linestyle='--', label=f'Peak at {shift_minutes} min')
ax2.set_title('Normalized Cross-Correlation Function')
ax2.set_xlabel('Time Lag $\\tau$ (minutes)')
ax2.set_ylabel('Correlation Coefficient')
ax2.legend()
ax2.grid()

plt.tight_layout()
plt.show()
