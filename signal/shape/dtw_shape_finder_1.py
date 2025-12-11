#!/usr/bin/env python3

"""
Animates the search for a specific shape/pattern within a larger signal
by continuously sliding a window, normalizing the segment, and comparing it 
against a defined target shape boundary using the Dynamic Time Warping (DTW) distance.
"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from datasets.sig_gallery import sig_exp_pulse


def dtw(s1: np.ndarray, s2: np.ndarray) -> float:
    """
    Calculates the Dynamic Time Warping (DTW) distance between two time series, s1 and s2.

    The DTW algorithm uses dynamic programming to find the minimum-cost path 
    to align the two sequences, allowing for temporal stretching and compression.

    Args:
        s1 (np.ndarray): The first time series (or subsequence/window).
        s2 (np.ndarray): The second time series (the target pattern).

    Returns:
        float: The DTW distance (the minimum accumulated cost).
    """
    n, m = len(s1), len(s2)

    # init the Accumulated Cost Matrix (ACM)
    # the matrix size is (n+1) x (m+1) to include the zero-indexed boundary conditions (init to infinity)
    cost_matrix = np.full((n + 1, m + 1), np.inf)
    cost_matrix[0, 0] = 0

    # fill the matrix using Dynamic Programming
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # calculate local cost (squared Euclidean distance between points s1[i-1] and s2[j-1])
            local_cost = (s1[i - 1] - s2[j - 1])**2

            # calculate the Minimum Accumulated Cost to reach cell (i, j)
            # it's the local cost plus the minimum cost of the three possible predecessors
            cost_matrix[i, j] = local_cost + min(
                # match s1[i] with s2[j] while continuing the alignment of s1 (horizontal step)
                cost_matrix[i - 1, j],
                # match s1[i] with s2[j] while continuing the alignment of s2 (vertical step)
                cost_matrix[i, j - 1],
                # match s1[i] with s2[j] (diagonal step: standard point-to-point alignment)
                cost_matrix[i - 1, j - 1]
            )

    # the DTW distance is the value in the bottom-right corner of the ACM
    # we take the square root to return a distance in the original Euclidean space (L1 or L2 norms).
    return np.sqrt(cost_matrix[n, m])


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
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
        self.fig.suptitle('Signal Shape Finder with DTW')
        self.ax3_dtw_l = []

    # plot animation function
    def _anim(self, frame: int):
        # to numpy
        start_at = frame
        raw_sig_part = self.raw_sig[start_at:self._window_size + start_at]

        # normalize signal
        if raw_sig_part.max() == raw_sig_part.min():
            sig = np.zeros_like(raw_sig_part)
        else:
            sig = 100 * (raw_sig_part - raw_sig_part.min()) / (raw_sig_part.max() - raw_sig_part.min()) - 100

        dtw_distance = dtw(sig, self.target_pat)
        sig_part_match = dtw_distance < self.threshold

        # ax infos
        ax_color = 'green' if sig_part_match else 'red'
        ax_label = f'DTW distance={dtw_distance:.2f} (frame {frame+1}/{self._frames})'

        # ax1 build (RAW signal)
        self.ax1.clear()
        self.ax1.plot(self.raw_sig, color='gray', label='Full RAW signal')
        self.ax1.plot(np.arange(self._window_size) + start_at, raw_sig_part,
                      color='blue', linewidth=2, label='Section analyzed')
        self.ax1.fill_between(np.arange(self._window_size) + start_at, raw_sig_part.min(),
                              raw_sig_part.max(), color=ax_color, alpha=0.1)
        self.ax1.set_ylabel('RAW signal value')
        self.ax1.grid()
        self.ax1.legend()

        # ax2 build (Normalized signal vs target pattern)
        self.ax2.clear()
        self.ax2.plot(sig, label='Signal', color='blue')
        self.ax2.plot(self.target_pat, 'r--', label='Target pattern')
        self.ax2.fill_between(self.x_axes, sig.min(), sig.max(), color=ax_color, alpha=0.1)
        self.ax2.set_ylabel('Normalized signal')
        self.ax2.legend()
        self.ax2.grid()

        # ax3 build (DTW Distance History)
        self.ax3_dtw_l.append(dtw_distance)
        self.ax3.plot(self.ax3_dtw_l, color='orange', label='Historique DTW')
        self.ax3.axhline(self.threshold, linestyle='--', color='green', label=f'Seuil={self.threshold:.2f}')
        self.ax3.set_xlabel(ax_label, fontdict={'color': ax_color})
        self.ax3.set_ylabel('DTW Distance')
        self.ax3.grid()

        return self.ax1, self.ax2, self.ax3

    def __call__(self):
        ani = animation.FuncAnimation(self.fig, self._anim, frames=self._frames, interval=150, repeat=False)
        plt.show()


if __name__ == '__main__':
    # fake raw signal
    raw_sig = 50 - 5*sig_exp_pulse(pulse_len=50, prefix_len=60, suffix_len=60)

    # target pattern
    target_pat = -100*sig_exp_pulse(pulse_len=50, prefix_len=10, suffix_len=0)

    # detection threshold
    threshold = 5.0

    ShapeFinderAnim(raw_sig, target_pat, threshold)()
