#!/usr/bin/env python3

from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


# some functions
def sigmoid(x, height: float, change_rate: float = -1.0, x_delta: float = 0.0):
    return height / (1 + np.exp(change_rate * (x - x_delta)))


# some class
class ShapeFinderAnim:
    def __init__(self, data_file_path: Path, frame_count: int) -> None:
        self.data_file_path = data_file_path
        self.frame_count = frame_count
        # load RAW signal from txt file
        self.full_raw_sig = np.genfromtxt(data_file_path, dtype=float)
        self.x = np.arange(self.frame_count)
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
        self.fig, (self.ax1, self.ax2) = plt.subplots(nrows=2, ncols=1)
        self.fig.suptitle('Signal shape finder')

    # plot animation function
    def animate(self, idx_frame: int):
        # to numpy
        sig_begin_at = idx_frame % 400
        sig = self.full_raw_sig[sig_begin_at:sig_begin_at + self.frame_count]

        # normalize signal from first value to %
        origin = max(sig[0], 10)
        norm_sig = (sig / origin) * 100
        norm_sig -= 100

        # check current limit and signal status
        up_overshoot = norm_sig - self.norm_sig_up
        up_overshoot[up_overshoot < 0] = 0.0
        down_overshoot = self.norm_sig_down - norm_sig
        down_overshoot[down_overshoot < 0] = 0.0
        mean_overshoot = (up_overshoot + down_overshoot).mean()
        sig_match = mean_overshoot < .2

        # ax1 build
        self.ax1.clear()
        self.ax1.plot(sig)
        self.ax1.set_ylabel('RAW signal value')
        self.ax1.grid()

        # ax2 build
        ax2_color = 'green' if sig_match else 'red'
        ax2_label = f'mean overshoot={mean_overshoot:.2f} % (frame {idx_frame+1}/{self.frame_count})'
        self.ax2.clear()
        self.ax2.plot(norm_sig, label='signal in %')
        self.ax2.plot(self.norm_sig_up, 'r--', label='max')
        self.ax2.plot(self.norm_sig_down, 'b--', label='min')
        self.ax2.fill_between(self.x, self.norm_sig_up, self.norm_sig_down, color=ax2_color, alpha=0.3)
        self.ax2.set_xlabel(ax2_label, fontdict={'color': ax2_color})
        self.ax2.set_ylabel('signal (in %)')
        self.ax2.legend()
        self.ax2.grid()

        return self.ax1, self.ax2

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=self.frame_count, interval=150, repeat=False)
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
    ShapeFinderAnim(data_file_path=data_file_path, frame_count=100).run()
