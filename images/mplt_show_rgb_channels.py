#!/usr/bin/env python3

"""Show RGB channels with matplotlib."""

from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


# some const
IMG_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Philips_PM5544.svg/1024px-Philips_PM5544.svg.png'

# load image
img = Image.open(urlopen(IMG_URL))
origin = np.array(img)

# create colors channels
r_channel = origin.copy()
r_channel[:, :, (1, 2)] = 0
g_channel = origin.copy()
g_channel[:, :, (0, 2)] = 0
b_channel = origin.copy()
b_channel[:, :, (0, 1)] = 0

# show colors channels with matplotlib
plt.imshow(np.concatenate((origin, r_channel, g_channel, b_channel), axis=1))
plt.show()
