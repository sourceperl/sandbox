#!/usr/bin/env python3

"""Lake basic model (as a prism): water height vs water missing volume."""

import numpy as np
import matplotlib.pyplot as plt


# some const
VOL_KM3 = 1.272
LENGTH_M = 22000
WIDTH_M = 1285
MAX_HEIGHT_M = 90

# compute water height (y axe) from missing volume of water (x axe)
missing_v = np.linspace(0, VOL_KM3, 1000)
k = WIDTH_M * LENGTH_M / MAX_HEIGHT_M
k = k / 2
height = np.sqrt((VOL_KM3 - missing_v) * 1e9 / k)
height = np.round(height, 1)

# define axes
plt.xlim(0.0, 1.4)
plt.xlabel('volume manquant (km3)')
plt.ylim(0, MAX_HEIGHT_M)
plt.yticks(np.arange(0, 100, 10))
plt.ylabel('hauteur d\'eau (m)')

# show grid major and minor
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

# plot
plt.plot(missing_v, height)
plt.show()
