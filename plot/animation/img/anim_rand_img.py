#!/usr/bin/env python3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use("Agg")


# init the writer
ff_writer = animation.writers['ffmpeg']
writer = ff_writer(fps=1, metadata=dict(title='My movie'))
fig = plt.figure()

# do animation stuff
with writer.saving(fig, 'animation.mp4', dpi=300):
    img_shape = (50, 50, 3)
    for i in range(10):
        img = np.random.random_sample(img_shape)
        plt.imshow(img)
        writer.grab_frame()
