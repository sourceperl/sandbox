#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)
y = 1 / (1 + np.exp(-x))
plt.plot(x, y)
plt.grid()
plt.show()
