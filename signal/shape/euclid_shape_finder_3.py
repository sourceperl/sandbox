#!/usr/bin/env python3

"""
Animates the search for a specific shape/pattern within a larger signal
by continuously sliding a window, normalizing the segment, and comparing it 
against a defined upper and lower shape boundary using a mean overshoot threshold.
"""


import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from datasets.sig_gallery import sig_exp_pulse


# some class
class ShapeFinderAnim:
    def __init__(self, frames: int, window_size: int, threshold: float = 1.0) -> None:
        self.frames = frames
        self.window_size = window_size
        self.threshold = threshold
        # load RAW signal from txt file
        self.raw_sig = 50 - 5*sig_exp_pulse(pulse_len=50, prefix_len=60, suffix_len=100)
        # target signal
        # self.sig_target = np.zeros(self.window_size)
        # self.sig_target[20:25] = -100
        # self.sig_target[25:30] = -50
        # self.sig_target[30:40] = -20
        # self.sig_target[40:50] = -10
        self.sig_target = -100*sig_exp_pulse(pulse_len=30, prefix_len=20, suffix_len=100)[:self.window_size]
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

        # normalize signal
        sig = 100 * (raw_sig_part - raw_sig_part.min()) / (raw_sig_part.max()-raw_sig_part.min()) - 100

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
    # start animation
    ShapeFinderAnim(frames=80, window_size=60).run()
