#!/usr/bin/env python3

# play DTMF frequency on current sound source

import numpy as np
from scipy.io import wavfile
import sounddevice


# some const
DTMF = {"1": (697, 1209), "2": (697, 1336), "3": (697, 1477), "A": (697, 1633),
        "4": (770, 1209), "5": (770, 1336), "6": (770, 1477), "B": (770, 1633),
        "7": (852, 1209), "8": (852, 1336), "9": (852, 1477), "C": (852, 1633),
        "*": (941, 1209), "0": (941, 1336), "#": (941, 1477), "D": (941, 1633)}


# some class
class Sound:
    def __init__(self):
        self.wav = []
        self.f_ech = 44100
        self.t_smp = 1 / self.f_ech
        self.level = 20000

    def tones(self, freq, duration=0.5):
        # ensure freq is a list
        if not type(freq) in (tuple, list):
            freq = [freq]
        # build n sample for specific duration
        n_smp = self._n_samples(duration)
        for t in np.linspace(0.0, self.t_smp * n_smp, n_smp):
            smp = 0
            # add every tones frequency
            for f in freq:
                smp += np.sin(2 * np.pi * f * t)
            # adjust to level with scale to avoid level overshoot
            smp = self.level * smp / len(freq)
            self.wav.append(smp)

    def pause(self, duration=0.5):
        self.wav.extend(np.zeros(self._n_samples(duration)))

    def play(self):
        sounddevice.play(np.array(self.wav, dtype=np.int16), samplerate=self.f_ech, blocking=True)

    def to_wav(self, file):
        wavfile.write(file, self.f_ech, np.array(self.wav, dtype=np.int16))

    def _n_samples(self, duration):
        return int(duration / self.t_smp)


# DTMF call 555-2358
sd = Sound()
# sd.tones(440, 1.0)
sd.pause()
for digit in "555 2368":
    if digit.isalnum():
        sd.tones(DTMF[digit], 0.4)
        sd.pause(0.2)
    else:
        sd.pause(0.8)
sd.play()
# sd.to_wav("555-2358.wav")
