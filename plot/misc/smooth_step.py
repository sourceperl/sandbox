#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def smooth_step(x, x_min, x_max):
    delta = x_max - x_min
    # scale to 0.0/1.0, clamp result to avoid overshooting
    x_p = (x - x_min) / delta
    x_p = np.clip(x_p, a_min=0.0, a_max=1.0)
    # smooth it (validity from 0.0 to 1.0, see https://en.wikipedia.org/wiki/Smoothstep)
    x_p = 3*x_p**2 - 2*x_p**3
    # rescale it
    x_smooth = x_p * delta + x_min
    return x_smooth


x = np.linspace(-100, 200, 1000)
y = smooth_step(x, x_min=0, x_max=100)
plt.plot(x, y)
plt.grid()
plt.show()
