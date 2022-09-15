#!/usr/bin/env python3

"""Build a random image from a numpy array."""

from random import randint
from PIL import Image
import numpy as np


a = np.zeros((200, 200, 3), np.uint8)
for x in range(a.shape[0]):
    for y in range(a.shape[1]):
        a[x, y] = [randint(0, 255), randint(0, 255), randint(0, 255)]
img = Image.fromarray(a, mode='RGB')
img.show()
