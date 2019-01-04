#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fftpack
import scipy.signal as signal
import time

# generating test signals
SAMPLE_RATE = 44100
WINDOW_SIZE = 2048
t = np.linspace(0, 1, SAMPLE_RATE)[:WINDOW_SIZE]

# build fake signal
y = np.sin(2 * np.pi * 50 * t)
y += np.sin(2 * np.pi * 500 * t)
y += np.sin(2 * np.pi * 750 * t)
y += np.sin(2 * np.pi * 10000 * t)
# add noise
y += (np.random.rand(WINDOW_SIZE)-0.5)*2*2
# normalize to +1.0/-1.0
y /= max(max(y), abs(min(y)))

# apply "hann" window to signal
y *= np.hanning(WINDOW_SIZE)

# FIR low-pass filter
# Nyquist rate of the signal.
nyq_rate = SAMPLE_RATE / 2
# The cutoff frequency of the filter: 15KHz
cutoff_hz = 15000
# create a lowpass FIR filter
fir_coeff = signal.firwin(numtaps=29, cutoff=cutoff_hz/nyq_rate)
# filter the signal with the FIR filter
y = signal.lfilter(fir_coeff, 1.0, y)

# fft
start = time.time()
yf = fftpack.fft(y)
yf = 1.0 / WINDOW_SIZE * np.abs(yf[:WINDOW_SIZE // 2])
xf = np.linspace(0.0, SAMPLE_RATE / 2, WINDOW_SIZE / 2)
end = time.time()
print("fft take %.4f s" % (end - start))
print("max: %.2f" % max(yf))

# plot data
plt.subplot(211)
plt.plot(t, y)
plt.ylabel("signal")
plt.grid()
plt.subplot(212)
plt.plot(xf, yf)
plt.ylabel("spectrum")
plt.grid()
plt.show()
