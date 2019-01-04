#!/usr/bin/env python3

# play DTMF frequency on current sound source

import numpy as np
from scipy.io import wavfile
import sounddevice


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
        #self.wav[-n_smp:] *= np.hamming(n_smp)

    def pause(self, duration=0.5):
        self.wav.extend(np.zeros(self._n_samples(duration)))

    def play(self):
        sounddevice.play(np.array(self.wav, dtype=np.int16), samplerate=self.f_ech, blocking=True)

    def to_wav(self, file):
        wavfile.write(file, self.f_ech, np.array(self.wav, dtype=np.int16))

    def _n_samples(self, duration):
        return int(duration / self.t_smp)


# play custom sound
notes = dict(c=522, d=586, e=658, f=698, g=784)

sd = Sound()
for n in "eeEeeEegcdE fffffeeeeddeDG":
    if n.isalpha():
        delay = 0.5 if n.islower() else 0.1
        sd.tones(notes[n.lower()], delay)
        sd.pause(0.05)
    else:
        sd.pause(0.1)
sd.play()
#sd.to_wav("/home/lefebvre/Musique/Sons/bells.wav")
