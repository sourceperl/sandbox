#!/usr/bin/env python3

from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

# define point tuple
Point = namedtuple('Point', 'x y')

# init multiplicator from Fibonacci sequence
for p1_m, p2_m in [(3, 5), (5, 8), (8, 13), (13, 21), (21, 34)]:
    # plot setup
    plt.axes().set_aspect(1)
    plt.axis('off')
    plt.title('flower for (%i,%i)' % (p1_m, p2_m))
    # draw
    for x in np.linspace(0, 2 * np.pi, 610):
        p1 = Point(np.cos(p1_m * x), np.sin(p1_m * x))
        p2 = Point(np.cos(p2_m * x), np.sin(p2_m * x))
        plt.plot((p1.x, p2.x),
                 (p1.y, p2.y), 'r-', alpha=0.3)
    # show it
    plt.show()
