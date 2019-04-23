#!/usr/bin/env python3

import argparse
import os.path
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile


# some function
def is_valid_file(filename):
    if not os.path.exists(filename):
        raise argparse.ArgumentTypeError("file %s does not exist" % filename)
    else:
        return filename


if __name__ == '__main__':
    # parse arg
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="input wav file",
                        type=lambda f: is_valid_file(f))
    args = parser.parse_args()
    # build wav spectrogram
    sample_rate, samples = wavfile.read(args.filename)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, nperseg=1024)
    # plot waterfall
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.colorbar()
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [sec]")
    plt.show()
