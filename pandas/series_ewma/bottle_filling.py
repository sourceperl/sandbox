#!/usr/bin/env python3

"""
Industrial Quality Control Simulation: EWMA Chart.

This script monitors a bottle-filling process (50cl target). 
It uses an Exponentially Weighted Moving Average (EWMA) to detect 
subtle process drifts before they exceed critical tolerance limits, 
triggering visual alerts when statistical control limits (3-sigma) are breached.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# simulate bottle filling data (target is 50cl)
# process is stable at first, then starts to drift upward
target_level = 50.0
levels = [50.1, 49.9, 50.0, 50.3, 49.8, 50.1, 49.9, 50.0, 49.9, 50.0,
          50.2, 50.3, 50.3, 50.4, 50.5, 50.6, 50.6, 50.7, 50.8, 50.9]

df = pd.DataFrame(levels, columns=['level'])

# configuration for the EWMA (Exponential Weighted Moving Average) control chart
# historical standard deviation of the machine
std_dev = 0.1
span = 5
alpha = 2 / (span + 1)
# sigma multiplier (standard for industrial quality control)
k = 3

# Calculate ewma
df['ewma'] = df['level'].ewm(span=span, adjust=False).mean()

# Calculate dynamic Control Limits
# As the EWMA accumulates data, the limits stabilize
df['upper_limit'] = target_level + k * std_dev * np.sqrt((alpha / (2 - alpha)))
df['lower_limit'] = target_level - k * std_dev * np.sqrt((alpha / (2 - alpha)))

# alert logic: 1 if EWMA is out of bounds, 0 otherwise
df['is_alert'] = (df['ewma'] > df['upper_limit']) | (df['ewma'] < df['lower_limit'])

# display the result to see when the drift is detected
df = df.round(3)
print(df)

plt.figure(figsize=(12, 6))

# Plot Control Limits (UCL/LCL)
plt.axhline(y=target_level, color='black', linestyle='--', alpha=0.5, label='Target (50cl)')
plt.plot(df['upper_limit'], color='red', linestyle='-', linewidth=1, label='Control Limits (3σ)')
plt.plot(df['lower_limit'], color='red', linestyle='-', linewidth=1)

# Fill the "Safe Zone" in light gray
plt.fill_between(df.index, df['lower_limit'], df['upper_limit'], color='gray', alpha=0.1)

# Plot Raw Data (faded to keep focus on the trend)
plt.scatter(df.index, df['level'], color='blue', alpha=0.3, label='Raw Measurements')

# Plot EWMA Trend
plt.plot(df['ewma'], color='blue', linewidth=2, marker='o', markersize=4, label='EWMA Trend')

# Highlight Alert Points in Red
alert_points = df[df['is_alert']]
plt.scatter(alert_points.index, alert_points['ewma'], color='red', s=100,
            edgecolors='black', zorder=5, label='⚠️ Quality Alert')

# Formatting
plt.title('Industrial Quality Control: EWMA Chart (Bottle Filling)', fontsize=14, pad=15)
plt.xlabel('Sample Number (Time)', fontsize=12)
plt.ylabel('Volume (cl)', fontsize=12)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True, which='both', linestyle=':', alpha=0.5)
plt.tight_layout()

plt.show()
