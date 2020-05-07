#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#  some functions
def sigmoid(x, height, change_rate=1.0, x_delta=0):
    return height / (1 + np.exp(change_rate * (x - x_delta)))


# load RAW signal from txt file
full_raw_sig = np.genfromtxt('raw_data.txt', dtype=float)


# plot animation function
def animate(i):
    # to numpy
    sig_begin_at = (i % 40) * 10
    sig = full_raw_sig[sig_begin_at:sig_begin_at + 101]

    # good model define
    x = np.arange(sig.size)
    mod_start_index = 17
    mod_max = .5

    # max part
    mod_max += sigmoid(x, -4.5, -1.1, mod_start_index + 4)
    mod_max += sigmoid(x, 2.0, -0.9, mod_start_index + 19)
    mod_max += sigmoid(x, -1.5, -0.9, mod_start_index + 50)

    # min part
    mod_min = -.5
    mod_min += sigmoid(x, -4.5, -1.1, mod_start_index)
    mod_min += sigmoid(x, 2.0, -0.9, mod_start_index + 21)
    mod_min += sigmoid(x, -1.5, -0.9, mod_start_index + 48)

    # normalize signal from first value to %
    origin = sig[0] if sig[0] > 10.0 else 10
    n_sig = 100 * sig / origin - 100

    # check current limit and signal status
    n_sig_up = n_sig - mod_max
    n_sig_up[n_sig_up < 0] = 0.0
    n_sig_down = mod_min - n_sig
    n_sig_down[n_sig_down < 0] = 0.0
    n_sig_over = n_sig_up + n_sig_down
    sig_dev = n_sig_over.mean()
    sig_match = sig_dev < .2

    # ax1 build
    ax1.clear()
    ax1.plot(sig)
    ax1.set_ylabel('RAW signal value')
    ax1.grid()

    # ax2 build
    ax2.clear()
    ax2.plot(n_sig, label='signal in %')
    ax2.plot(mod_max, 'r--', label='max')
    ax2.plot(mod_min, 'b--', label='min')
    ax2.fill_between(x, mod_max, mod_min, color='green' if sig_match else 'red', alpha=0.3)
    ax2.set_xlabel('mean deviation=%.2f %%' % sig_dev,
                   fontdict=dict(color='green' if sig_match else 'red'))
    ax2.set_ylabel('signal deviation (in %)')
    ax2.legend()
    ax2.grid()


fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
fig.canvas.set_window_title('Signal shape finder')
ani = animation.FuncAnimation(fig, animate, interval=1000)
fig.autofmt_xdate()
plt.show()
