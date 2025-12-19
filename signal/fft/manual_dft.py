#!/usr/bin/env python3

"""
Spectrum Analysis via Manual Discrete Fourier Transform (DFT).

This script generates a signal composed of multiple sine waves, calculates the DFT
using the fundamental mathematical formula (without high-level black-box functions),
and displays both the double-sided spectrum (positive and negative frequencies) 
and the corrected single-sided amplitude spectrum.

Key concepts demonstrated:
- Temporal sampling parameters (Fs, N).
- Complex magnitude calculation: sqrt(Re^2 + Im^2).
- Amplitude normalization (1/N for double-sided, 2/N for single-sided).
- Frequency axis reconstruction and aliasing management.
"""

import matplotlib.pyplot as plt
import numpy as np

# build signal (N=200 samples at Fs=800 Hz -> 0.25 second of data)
N = 200
Fs = 800
t = np.arange(N) / Fs

x = 1.0 * np.sin(2*np.pi*200.0*t)
x += 1.0 * np.sin(2*np.pi*100.0*t)

# manual DFT
X = np.zeros(N, dtype=complex)
for k in range(0, N):
    for n in range(0, N):
        X[k] += x[n] * np.exp(-1j * 2 * np.pi * k * n / N)

# manual magnitude calculation & normalization
X_magnitude = np.sqrt(X.real**2 + X.imag**2)
X_magnitude /= N

# numpy DFT for comparison
X_NP_magnitude = np.abs(np.fft.fft(x))
X_NP_magnitude /= N

# manual frequency axis build
X_freqs = np.zeros(N)
for k in range(N):
    if k < N / 2:
        # positive frequencies [0, Fs/2[
        X_freqs[k] = Fs * k / N
    else:
        # negative frequencies [-Fs/2, 0[
        X_freqs[k] = Fs * (k - N) / N

# sort frequencies so the plot is a continuous line
sort_indices = np.argsort(X_freqs)
X_freqs_sorted = X_freqs[sort_indices]
X_magnitude_sorted = X_magnitude[sort_indices]
X_NP_mag_sorted = X_NP_magnitude[sort_indices]

# show results
# !!! since we are keeping the frequencies negative, the amplitudes will be reduced by half !!!
plt.figure(figsize=(10, 8))

plt.subplot(311)
plt.title("Time Domain")
plt.plot(t, x)
plt.ylabel("Amplitude")
plt.grid()

plt.subplot(312)
plt.title("Frequency Domain (NumPy FFT)")
plt.plot(X_freqs_sorted, X_NP_mag_sorted, label='numpy fft', color='tab:orange')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.legend()

plt.subplot(313)
plt.title("Frequency Domain (Manual DFT)")
plt.plot(X_freqs_sorted, X_magnitude_sorted, label='manual fft', color='tab:blue')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
