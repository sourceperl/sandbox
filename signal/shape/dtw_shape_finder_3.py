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


def dtw(s1: np.ndarray, s2: np.ndarray) -> tuple[float, list[tuple[int, int]]]:
    """
    Calculates the DTW distance and the optimal warping path.

    Args:
        s1 (np.ndarray): The first time series (segment).
        s2 (np.ndarray): The second time series (target pattern).

    Returns:
        tuple[float, list[tuple[int, int]]]: (DTW distance, list of (s1_idx, s2_idx) pairs)
    """
    n, m = len(s1), len(s2)
    # init the Accumulated Cost Matrix (ACM)
    cost_matrix = np.full((n + 1, m + 1), np.inf)
    cost_matrix[0, 0] = 0

    # fill the matrix (forward pass)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            local_cost = (s1[i - 1] - s2[j - 1])**2
            cost_matrix[i, j] = local_cost + min(
                cost_matrix[i - 1, j],
                cost_matrix[i, j - 1],
                cost_matrix[i - 1, j - 1]
            )

    distance = np.sqrt(cost_matrix[n, m])

    # backtracking to find the optimal path
    path = []
    i, j = n, m

    while i > 0 or j > 0:
        # store 0-based indices
        path.append((i - 1, j - 1))

        if i == 0 and j == 0:
            break

        # determine the costs of predecessors
        cost_diag = cost_matrix[i - 1, j - 1] if i > 0 and j > 0 else np.inf
        cost_horiz = cost_matrix[i - 1, j] if i > 0 else np.inf
        cost_vert = cost_matrix[i, j - 1] if j > 0 else np.inf
        min_cost = min(cost_diag, cost_horiz, cost_vert)

        # move to the predecessor with the minimum cost
        if min_cost == cost_diag:
            i -= 1
            j -= 1
        elif min_cost == cost_horiz:
            i -= 1
        elif min_cost == cost_vert:
            j -= 1
        else:
            break

    path.reverse()
    return distance, path


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
        start_at = frame
        raw_sig_part = self.raw_sig[start_at:self._window_size + start_at]

        # normalize signal
        if raw_sig_part.max() == raw_sig_part.min():
            sig = np.zeros_like(raw_sig_part)
        else:
            sig = 100 * (raw_sig_part - raw_sig_part.min()) / (raw_sig_part.max() - raw_sig_part.min()) - 100

        dtw_distance, dtw_path = dtw(sig, self.target_pat)
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

        # ax2 build (normalized signal vs target pattern with alignment lines)
        self.ax2.clear()
        self.ax2.plot(self.x_axes, sig, label='Segment', color='blue')
        self.ax2.plot(self.x_axes, self.target_pat, 'r--', label='Target pattern')
        self.ax2.fill_between(self.x_axes, sig.min(), sig.max(), color=ax_color, alpha=0.1)
        # draw the alignment lines based on the DTW path
        for i, j in dtw_path:
            self.ax2.plot([i, i], [sig[i], self.target_pat[j]], 'k:', linewidth=0.8, alpha=0.5)
        self.ax2.set_ylabel('Normalized signal')
        self.ax2.legend()
        self.ax2.grid()

        # ax3 build (DTW distance history)
        self.ax3.clear()
        self.ax3_dtw_l.append(dtw_distance)
        self.ax3.plot(self.ax3_dtw_l, color='orange', label='DTW distance')
        self.ax3.axhline(self.threshold, linestyle='--', color='green', label=f'Seuil={self.threshold:.2f}')
        self.ax3.set_xlabel(ax_label, fontdict={'color': ax_color})
        self.ax3.set_ylabel('DTW Distance')
        self.ax3.legend()
        self.ax3.grid()

        return self.ax1, self.ax2, self.ax3

    def __call__(self):
        ani = animation.FuncAnimation(self.fig, self._anim, frames=self._frames, interval=200, repeat=False)
        plt.show()


if __name__ == '__main__':
    # fake raw signal
    raw_sig = np.concatenate([np.zeros(50),
                              -10 * sig_exp_pulse(pulse_len=50),
                              np.zeros(100),
                              -20 * sig_exp_pulse(pulse_len=50),])
    raw_sig += 500
    raw_sig[100:] -= 15
    raw_sig[110:] += 10
    raw_sig[120:] += 10
    # add gaussian noise
    raw_sig += np.random.normal(loc=0.0, scale=0.2, size=raw_sig.shape)

    # target pattern
    target_pat = np.zeros(50)
    target_pat[10:15] = -100
    target_pat[15:20] = -50
    target_pat[20:30] = -20
    target_pat[30:40] = -10

    # detection threshold
    threshold = 60.0

    ShapeFinderAnim(raw_sig, target_pat, threshold)()
