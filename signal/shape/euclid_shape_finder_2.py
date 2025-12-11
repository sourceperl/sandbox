#!/usr/bin/env python3

"""
Animates the search for a specific shape/pattern within a larger raw signal
by continuously sliding a window, normalizing the segment, and comparing it 
against a defined upper and lower shape boundary using a mean overshoot threshold.
"""


from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


# some class
class ShapeFinderAnim:
    def __init__(self, raw_sig: np.ndarray, target_pat: np.ndarray, threshold: float) -> None:
        # public
        self.raw_sig = raw_sig
        self.target_pat = target_pat
        self.threshold = threshold
        # private
        self._window_size = len(self.target_pat)
        self._frames = len(self.raw_sig) - self._window_size

        # x axis
        self.x_axes = np.arange(self._window_size)
        # init subplots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows=3, ncols=1)
        self.fig.suptitle('Signal shape finder (euclidean distance)')
        self.ax3_y = [None] * self._frames

    # plot animation function
    def _anim(self, frame: int):
        # to numpy
        start_at = frame
        raw_sig_part = self.raw_sig[start_at:self._window_size + start_at]

        # normalize signal from first value to %
        origin = raw_sig_part[0]
        sig = (raw_sig_part / origin) * 100
        sig -= 100

        # check current limit and signal status
        square_overshoot = (sig - self.target_pat)**2
        mean_overshoot = np.sqrt(square_overshoot.mean())
        sig_part_match = mean_overshoot < self.threshold

        # ax infos
        ax_color = 'green' if sig_part_match else 'red'
        ax_label = f'mean overshoot={mean_overshoot:.2f} % (frame {frame+1}/{self._frames})'

        # ax1 build
        self.ax1.clear()
        self.ax1.plot(self.raw_sig, color='gray', label='Full RAW signal')
        self.ax1.plot(np.arange(self._window_size) + start_at, raw_sig_part,
                      color='blue', linewidth=2, label='Section analyzed')
        self.ax1.fill_between(np.arange(self._window_size) + start_at, raw_sig_part.min(),
                              raw_sig_part.max(), color=ax_color, alpha=0.1)
        self.ax1.set_ylabel('RAW signal value')
        self.ax1.grid()

        # ax2 build
        self.ax2.clear()
        self.ax2.plot(sig, label='Signal')
        self.ax2.plot(self.target_pat, 'r--', label='Target pattern')
        self.ax2.fill_between(self.x_axes, sig, self.target_pat, color=ax_color, alpha=0.3)
        self.ax2.set_ylabel('signal (in %)')
        self.ax2.legend()
        self.ax2.grid()

        # ax3 build
        self.ax3_y[frame] = mean_overshoot
        self.ax3.plot(self.ax3_y, color='orange')
        self.ax3.axhline(self.threshold, linestyle='--', color='green')
        self.ax3.set_xlabel(ax_label, fontdict={'color': ax_color})
        self.ax3.set_ylabel('mean overshoot (in %)')
        self.ax3.grid()

        return self.ax1, self.ax2, self.ax3

    def __call__(self):
        ani = animation.FuncAnimation(self.fig, self._anim, frames=self._frames, interval=150, repeat=False)
        # movie save (duration (in s) = frames * 1 / fps)
        # ani.save('out.mp4', fps=10, dpi=300)
        # display animation (duration (in s) = frames * interval / 1000)
        plt.show()


if __name__ == '__main__':
    # raw_data.txt path is relative to script path
    script_dir = Path(__file__).resolve().parent
    data_file_path = script_dir / 'datasets/raw_data.txt'
    # load RAW signal from txt file
    raw_sig = np.genfromtxt(data_file_path, dtype=float)
    # target signal
    target_pat = np.zeros(80)
    target_pat[19:37] = -4.5
    target_pat[37:66] = -2.5
    target_pat[66:] = -4

    # detection threshold
    threshold = 1.0

    ShapeFinderAnim(raw_sig, target_pat, threshold)()
