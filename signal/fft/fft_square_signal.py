#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import fftpack

# number of samples
Ns = 2000

# second between 2 samples
Ts = 100e-6  # 100 us

# N samples, every sample is time value (in s)
# 0 -> t_max with Ns items
t_max = Ts * Ns
t_samples = np.linspace(0.0, t_max, Ns)

# build square signal at 50 Hz
f = 50.0
w = 2 * np.pi * f

# by scipy signal (pure square)
y_samples = np.zeros(Ns)
y_samples += signal.square(w * t_samples, duty=0.5) * 2 + 2

# build signal
nb = len(y_samples)
x = np.linspace(0.0, (nb - 1) * Ts, nb)

# compute fft
yf = fftpack.fft(y_samples)
xf = np.linspace(0.0, 1.0 / (2.0 * Ts), nb // 2)
ya = 2.0 / nb * np.abs(yf[:nb // 2])

# plot 1 data
plt.subplot(211)
plt.plot(x, y_samples)
plt.grid()

# plot 2 spectrum
plt.subplot(212)
plt.plot(xf, ya)
plt.show()
