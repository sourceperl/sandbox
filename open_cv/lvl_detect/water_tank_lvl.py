#!/usr/bin/env python

import os
import imutils
import matplotlib.pyplot as plt
import numpy as np
import cv2

# image file path (relative to this script path)
img_file = os.path.join(os.path.dirname(__file__), "img/water_tank.jpg")

# load image and crop it
img_full = cv2.imread(img_file)
img = img_full[268:938, 464:564].copy()

# gray histogram
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hist_g = cv2.calcHist([img_g], [0], None, [256], [0, 256])

# threshold gray image at 180 intensity value
_, img_g_th = cv2.threshold(img_g, 180, 255, cv2.THRESH_BINARY)

# erode test img
kernel = np.ones((4, 4), np.uint8)
img_th_e = cv2.erode(img_g_th, kernel, iterations=3)

# search and draw contour
if imutils.is_cv3():
    _, contours, _ = cv2.findContours(img_th_e.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
else:
    contours, _ = cv2.findContours(img_th_e.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_g, contours, -1, (0, 0, 0), 10)

# areas compute
msg = "empty area not found"
if len(contours) == 1:
    area = cv2.contourArea(contours[0])
    img_area = img.shape[0] * img.shape[1]
    percent_usage = 100 - 100 * area / img_area
    volume = 1000 * percent_usage / 100
    msg = "area = %.f px\nimg = %.f px\n\nlevel = %.2f %%\nvolume = %.f l"
    msg %= (area, img_area, percent_usage, volume)

# display results
plt.figure(num="Water tank level detector")
plt.subplot(2, 3, 1)
plt.title("full img")
plt.imshow(imutils.opencv2matplotlib(img_full))
plt.subplot(2, 3, 2)
plt.title("img with crop")
plt.imshow(img_g, cmap="gray")
plt.subplot(2, 3, 3)
plt.title("gray histogram")
plt.plot(hist_g)
plt.subplot(2, 3, 4)
plt.title("threshold img")
plt.imshow(img_g_th, cmap="gray")
plt.subplot(2, 3, 5)
plt.title("erode threshold img")
plt.imshow(img_th_e, cmap="gray")
ax = plt.subplot(2, 3, 6)
ax.axis("off")
ax.text(0.5, 0.5, msg, horizontalalignment='center', verticalalignment='center')
plt.show()
