import os
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import pandas as pd

# set current workdir to script path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# load CSV file as dataframe
df = pd.read_csv('data/loto_201911.csv', sep=';')

# concatenate all ball columns into one flat list
ball_cols = ['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']
all_balls = df[ball_cols].melt()['value'].dropna().astype(int).tolist()

# count occurrences of each number
counts = Counter(all_balls)

# ensure all numbers from 1 to 49 are represented (even if 0 occurrences)
n = len(all_balls)
x = list(range(1, 50))
y = [100 * counts[num]/n for num in x]

# calculate mean probability
# theoretical expected value is 100 / 49 (~2.04%)
mean = float(np.mean(y))
std = float(np.std(y, ddof=0))

# plotting frequency counts
plt.figure(figsize=(12, 4))
plt.bar(x, y, color='tab:blue', alpha=0.7, edgecolor='black', label='observed')

# add horizontal line for mean
plt.axhline(y=mean, color='green', linestyle='--', linewidth=1.5, label=f'mean ({mean:.2f}%)')

# add shaded bands for 1, 2 and 3 standard deviations (outer to inner for proper visual layering)
plt.axhspan(mean - 3 * std, mean + 3 * std, color='red', alpha=0.10,
            label=f'±3σ ({mean - 3*std:.2f}% à {mean + 3*std:.2f}%)')
plt.axhspan(mean - 2 * std, mean + 2 * std, color='orange', alpha=0.15,
            label=f'±2σ ({mean - 2*std:.2f}% à {mean + 2*std:.2f}%)')
plt.axhspan(mean - std, mean + std, color='green', alpha=0.20,
            label=f'±1σ ({mean - std:.2f}% à {mean + std:.2f}%)')

plt.title('Occurrences per ball number (boules 1 to 5) since november 2019')
plt.xlabel('Lotto balls')
plt.ylabel('Probability (%)')
plt.xlim(0, 50)
plt.ylim(1.4, 2.6)

# set x-axis ticks every 2 units
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
