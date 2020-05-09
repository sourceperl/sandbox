#!/usr/bin/env python3

import numpy as np
from scipy.signal import butter, lfilter, freqz, square, periodogram
import matplotlib.pyplot as plt


# some functions
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


# filter requirements
# sampling at 10 KHz
fs = 10000
ts = 1 / fs
# low and high cut frequency
f_l_cut = 1400
f_h_cut = 1600

# get filter coefficients (Butterworth filter IIR)
b, a = butter_bandpass(f_l_cut, f_h_cut, fs)

# build signal (500 Hz square)
measure_t = 0.04
nb_sample = round(measure_t / ts)
t = np.linspace(0, measure_t, nb_sample)
y = square(2 * np.pi * 500 * t)

# apply filter
y_filtered = lfilter(b, a, y)

# plot frequency response
plt.subplot(311)
w, h = freqz(b, a, worN=8000)
plt.plot(0.5 * fs * w / np.pi, np.abs(h))
plt.axvline(f_l_cut, color='b')
plt.axvline(f_h_cut, color='r')
plt.plot(f_l_cut, 0.5 * np.sqrt(2), 'ko')
plt.plot(f_h_cut, 0.5 * np.sqrt(2), 'ko')
plt.xlim(0, 0.25 * fs)
plt.ylabel('resp. [ratio/Hz]')
plt.grid()

plt.subplot(312)
plt.plot(t, y, label='y', color='firebrick')
plt.plot(t, y_filtered, label='y filtered', color='goldenrod')
plt.ylabel('[signal/time (s)]')
plt.grid()
plt.legend()

plt.subplot(313)
f, Pxx_den = periodogram(y, fs)
plt.plot(f, Pxx_den, label='y', color='firebrick')
f, Pxx_den = periodogram(y_filtered, fs)
plt.plot(f, Pxx_den, label='y filtered', color='goldenrod')
plt.axvline(f_l_cut, color='b')
plt.axvline(f_h_cut, color='r')
plt.xlim(0, 0.25 * fs)
plt.ylabel('PSD [V**2/Hz]')
plt.grid()
plt.legend()
plt.show()
