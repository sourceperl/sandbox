"""Calculates the Fast Fourier Transform (FFT) of a composite signal, use the numpy fft."""

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import rfft, rfftfreq

# build a 1000 samples signal
N = 1_000
Fs = 1_000
t = np.arange(N)/Fs

# DC + 50 Hz sin + 200 Hz sin + 300 Hz sin
signal = 0.5
signal += 1.0 * np.sin(2*np.pi*50*t)
signal += 0.6 * np.sin(2*np.pi*200*t)
signal += 1.0 * np.sin(2*np.pi*300*t)

# FFT
# Note: for rfft, you only multiply amplitude by 2.0 for 1:end-1 because the DC (0)
# and the Nyquist (end) terms don't have a negative-frequency counterpart.
amplitudes = np.abs(rfft(signal, norm='forward'))
amplitudes[1:-1] *= 2.0
freqs = rfftfreq(N, d=1/Fs)

#  plot
plt.plot(freqs, amplitudes)
plt.title('Normalized FFT spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()
