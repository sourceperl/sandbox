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
    def __init__(self, data_file_path: Path, frames: int, window_size: int, threshold: float = 1.0) -> None:
        self.data_file_path = data_file_path
        self.frames = frames
        self.window_size = window_size
        self.threshold = threshold
        # load RAW signal from txt file
        self.raw_sig = np.genfromtxt(data_file_path, dtype=float)
        # target signal
        self.sig_target = np.zeros(self.window_size)
        self.sig_target[19:37] = -4.5
        self.sig_target[37:66] = -2.5
        self.sig_target[66:] = -4
        # x axis
        self.x_axes = np.arange(self.window_size)
        # init subplots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows=3, ncols=1)
        self.fig.suptitle('Signal shape finder')
        self.ax3_y = [None] * self.frames

    # plot animation function
    def _anim(self, frame: int):
        # to numpy
        start_at = frame
        raw_sig_part = self.raw_sig[start_at:self.window_size + start_at]

        # normalize signal from first value to %
        origin = raw_sig_part[0]
        sig = (raw_sig_part / origin) * 100
        sig -= 100

        # check current limit and signal status
        square_overshoot = (sig - self.sig_target)**2
        mean_overshoot = np.sqrt(square_overshoot.mean())
        sig_part_match = mean_overshoot < self.threshold

        # ax infos
        ax_color = 'green' if sig_part_match else 'red'
        ax_label = f'mean overshoot={mean_overshoot:.2f} % (frame {frame+1}/{self.frames})'

        # ax1 build
        self.ax1.clear()
        self.ax1.plot(raw_sig_part)
        self.ax1.set_ylabel('RAW signal value')
        self.ax1.grid()

        # ax2 build
        self.ax2.clear()
        self.ax2.plot(sig, label='signal in %')
        self.ax2.plot(self.sig_target, 'r--', label='max')
        self.ax2.fill_between(self.x_axes, sig, self.sig_target, color=ax_color, alpha=0.3)
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

    def run(self):
        ani = animation.FuncAnimation(self.fig, self._anim, frames=self.frames, interval=150, repeat=False)
        # movie save (duration (in s) = frames * 1 / fps)
        # mp4_path = self.data_file_path.parent / 'out.mp4'
        # ani.save(mp4_path, fps=10, dpi=300)
        # display animation (duration (in s) = frames * interval / 1000)
        plt.show()


if __name__ == '__main__':
    # raw_data.txt path is relative to script path
    script_dir = Path(__file__).resolve().parent
    data_file_path = script_dir / 'datasets/raw_data.txt'
    # start animation
    ShapeFinderAnim(data_file_path=data_file_path, frames=200, window_size=100).run()
