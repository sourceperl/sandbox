#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile

# some consts
F_SAMPLE = 44100
DURATION_S = 10.0
ATTENUATION = 0.5
WAV_FILE = "strange.wav"

# some vars
t_sample = 1 / F_SAMPLE

# init empty waveform
waveform = np.zeros(int(DURATION_S * F_SAMPLE))

# add samples
for i, v in enumerate(waveform):
    t = i * t_sample
    waveform[i] += np.sin(2 * np.pi * 20 * (np.sin(2 * np.pi * 0.5 * t))**2 * (np.sin(2 * np.pi * 3.0 * t))**2 * t)

# write to wav file
scaled = np.int16(waveform / np.max(np.abs(waveform)) * 2**16//2 * ATTENUATION)
wavfile.write(WAV_FILE, F_SAMPLE, scaled)
