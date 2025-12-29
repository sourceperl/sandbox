#!/usr/bin/env python3

"""Show RGB channels with matplotlib."""

from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# some const
IMG_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/L%C3%A1pices_de_colores_01.jpg/1024px-L%C3%A1pices_de_colores_01.jpg'

# load image
img = Image.open(urlopen(Request(IMG_URL, headers={'User-Agent': 'MyApp/1.0'})))
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
