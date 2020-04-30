#!/usr/bin/env python3
from collections import namedtuple
from math import sin, cos
import matplotlib.pyplot as plt

STEPS = 1000

# define point tuple
Point = namedtuple('Point', 'x y')

p1 = Point(0.0, 0.0)

# walk loop
for i in range(STEPS):
    red = i/STEPS
    p2 = Point(p1.x + sin(i ** 3) * 0.125 + sin(i ** 2) * 0.075,
               p1.y + cos(i ** 2) * 0.25 + sin(i ** 2) * 0.075)
    plt.plot((p1.x, p2.x), (p1.y, p2.y), color=(red, 0.0, 0.0), alpha=0.3)
    p1 = p2

# show it
plt.show()
