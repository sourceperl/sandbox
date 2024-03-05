#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# data
x = np.array([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
y = np.array([10.35, 12.3, 13, 12.5, 16, 19.5, 18.2, 20, 20.7, 22.5])

# linear regress
gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)

mn = np.min(x)
mx = np.max(x)
x1 = np.linspace(mn, mx, 500)
y1 = gradient * x1 + intercept
print('y = %.2f * x + %.2f' % (gradient, intercept))

# plot
plt.plot(x, y, 'ob')
plt.plot(x1, y1, '-r')
plt.show()
