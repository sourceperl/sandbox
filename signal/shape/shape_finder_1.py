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


# some functions
def sigmoid(x, height: float, change_rate: float = -1.0, x_delta: float = 0.0):
    return height / (1 + np.exp(change_rate * (x - x_delta)))


# some class
class ShapeFinderAnim:
    def __init__(self, data_file_path: Path, frames: int, window_size: int, threshold: float = 0.2) -> None:
        self.data_file_path = data_file_path
        self.frames = frames
        self.window_size = window_size
        self.threshold = threshold
        # load RAW signal from txt file
        self.full_raw_sig = np.genfromtxt(data_file_path, dtype=float)
        self.x = np.arange(self.window_size)
        # good model define
        mod_start_index = 17
        # max part
        self.norm_sig_up = .5
        self.norm_sig_up += sigmoid(self.x, -4.5, -1.1, mod_start_index + 4)
        self.norm_sig_up += sigmoid(self.x, 2.0, -0.9, mod_start_index + 19)
        self.norm_sig_up += sigmoid(self.x, -1.5, -0.9, mod_start_index + 50)
        # min part
        self.norm_sig_down = -.5
        self.norm_sig_down += sigmoid(self.x, -4.5, -1.1, mod_start_index)
        self.norm_sig_down += sigmoid(self.x, 2.0, -0.9, mod_start_index + 21)
        self.norm_sig_down += sigmoid(self.x, -1.5, -0.9, mod_start_index + 48)
        # init subplots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows=3, ncols=1)
        self.fig.suptitle('Signal shape finder')
        self.ax3_y = [None] * self.frames

    # plot animation function
    def _anim(self, frame: int):
        # to numpy
        start_at = frame
        sig_part = self.full_raw_sig[start_at:self.window_size + start_at]

        # normalize signal from first value to %
        origin = max(sig_part[0], 10)
        norm_sig_part = (sig_part / origin) * 100
        norm_sig_part -= 100

        # check current limit and signal status
        up_overshoot = norm_sig_part - self.norm_sig_up
        up_overshoot[up_overshoot < 0] = 0.0
        down_overshoot = self.norm_sig_down - norm_sig_part
        down_overshoot[down_overshoot < 0] = 0.0
        mean_overshoot = (up_overshoot + down_overshoot).mean()
        sig_part_match = mean_overshoot < self.threshold

        # ax infos
        ax_color = 'green' if sig_part_match else 'red'
        ax_label = f'mean overshoot={mean_overshoot:.2f} % (frame {frame+1}/{self.frames})'

        # ax1 build
        self.ax1.clear()
        self.ax1.plot(sig_part)
        self.ax1.set_ylabel('RAW signal value')
        self.ax1.grid()

        # ax2 build
        self.ax2.clear()
        self.ax2.plot(norm_sig_part, label='signal in %')
        self.ax2.plot(self.norm_sig_up, 'r--', label='max')
        self.ax2.plot(self.norm_sig_down, 'b--', label='min')
        self.ax2.fill_between(self.x, self.norm_sig_up, self.norm_sig_down, color=ax_color, alpha=0.3)
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
    data_file_path = script_dir / 'raw_data.txt'
    # start animation
    ShapeFinderAnim(data_file_path=data_file_path, frames=200, window_size=100).run()
