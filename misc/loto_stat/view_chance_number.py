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

# extract chance numbers series
chance_nums = df['numero_chance'].dropna().astype(int)

# count occurrences of each number
counts = Counter(chance_nums)

# calculate percentage occurrences for numbers 1 to 10
n = len(chance_nums)
x = list(range(1, 11))
y = [100 * counts[num]/n for num in x]

# calculate mean (theoretical expected value is 10%) and standard deviation
mean = float(np.mean(y))
std = float(np.std(y, ddof=1))

# plotting frequency counts
plt.figure(figsize=(12, 4))
plt.bar(x, y, color='tab:blue', alpha=0.7, edgecolor='black', label='observed')

# add horizontal line for mean 
plt.axhline(y=mean, color='green', linestyle='--', linewidth=1.5, label=f'mean ({mean:.2f}%)')

# add shaded bands for 1, 2 and 3 standard deviations
plt.axhspan(mean - 3 * std, mean + 3 * std, color='red', alpha=0.10,
            label=f'±3σ ({mean - 3*std:.2f}% à {mean + 3*std:.2f}%)')
plt.axhspan(mean - 2 * std, mean + 2 * std, color='orange', alpha=0.15,
            label=f'±2σ ({mean - 2*std:.2f}% à {mean + 2*std:.2f}%)')
plt.axhspan(mean - std, mean + std, color='green', alpha=0.20,
            label=f'±1σ ({mean - std:.2f}% à {mean + std:.2f}%)')

plt.title(f'Occurrences of chance numbers since november 2019 ({len(df)} draws)')
plt.xlabel('Chance number')
plt.ylabel('Probability (%)')
plt.ylim(6.0, 14.0)

# set x-axis ticks to every integer from 1 to 10
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
