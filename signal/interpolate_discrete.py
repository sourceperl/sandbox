#!/usr/bin/env python3

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# data
y = np.array([4, 2, 6, 7, 5, 8, 9, 10, 11, 15, 14, 12])
x = np.linspace(0, 4, len(y))

# interpolate
f_linear = interp1d(x, y, kind='linear')
f_cubic = interp1d(x, y, kind='cubic')
x_new = np.linspace(0, 4, 300)

# plot
plt.plot(x, y, 'o')
plt.plot(x_new, f_linear(x_new), '-')
plt.plot(x_new, f_cubic(x_new), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.grid()
plt.show()
