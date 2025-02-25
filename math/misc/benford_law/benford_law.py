import csv
import gzip
import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

# set current workdir to script path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# open gzipped CSV
with gzip.open('communes.csv.gz', 'r') as f:
    csv_data = f.read().decode()

# extract the “Population” field, keep the first non-zero digit
first_digit_l = []
for row in csv.DictReader(csv_data.splitlines(), delimiter=','):
    for char in row['Population']:
        if char != '0':
            first_digit_l.append(int(char))
            break

# count all digits from 1 to 9
occurrences = Counter(first_digit_l)
total = sum(occurrences.values())
digits_pct = {item: (count / total) * 100 for item, count in occurrences.items()}

# theoretical data
x = np.linspace(1, 9, 100)
y = np.log10(1 + (1/x)) * 100

# plot results
plt.plot(x, y, color='darkorange')
plt.bar(list(digits_pct.keys()), list(digits_pct.values()), color='bisque')
plt.xticks(range(1, 10))
plt.title('Benford\'s law')
plt.xlabel('Digits')
plt.ylabel('Frequency (%)')
plt.grid()
plt.show()
