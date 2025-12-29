#!/usr/bin/env python3

"""Decode position of a gauge needle."""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# load image
current_dir = Path(__file__).resolve().parent
pil_origin_img = Image.open(current_dir / 'img/gauge.jpg')
origin_img = np.array(pil_origin_img)

# step 1: perspective change
# define quadrilateral corners to map to a rectangle
c1, c2 = [166, 164], [718, 157]
c4, c3 = [169, 765], [721, 773]
src_corners = np.float32([c1, c2, c3, c4])
dst_corners = np.float32([[0, 0], [pil_origin_img.width - 1, 0],
                          [pil_origin_img.width - 1, pil_origin_img.height - 1], [0, pil_origin_img.height - 1]])
# apply change, create flatted image
matrix = cv2.getPerspectiveTransform(src_corners, dst_corners)
flat_img = cv2.warpPerspective(origin_img, matrix, (pil_origin_img.width, pil_origin_img.height), cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

# step2: select by colors
# set lower and upper selected colors limits
low_color = np.array([0, 0, 0])
up_color = np.array([80, 80, 80])
flat_img_mask = cv2.inRange(cv2.cvtColor(flat_img, cv2.COLOR_BGR2HSV), low_color, up_color)

# step3: find needle line and add it to flat image
th, th_gray_mask = cv2.threshold(flat_img_mask, thresh=175, maxval=255, type=cv2.THRESH_BINARY)
lines_l = cv2.HoughLinesP(th_gray_mask, rho=3, theta=np.pi / 180, threshold=100, minLineLength=220)
(x_center, y_center) = (501, 530)
if lines_l is not None:
    for line_l in lines_l:
        for (x1, y1, x2, y2) in line_l:
            x_end = max(x1, x2, key=lambda i: abs(i - x_center))
            y_end = max(y1, y2, key=lambda i: abs(i - y_center))
            line_len = round(np.sqrt((x_end - x_center) ** 2 + (y_end - y_center) ** 2))
            if x_end < x_center:
                line_ang = 90 + np.degrees(np.arcsin((y_center - y_end) / line_len))
            else:
                line_ang = 180 + 90 - np.degrees(np.arcsin((y_center - y_end) / line_len))
            pressure = ((line_ang - 42) / 276) * 2500
            # print current line stats
            print(f'find a line from {(x1, y1)} to {(x2, y2)}')
            print(f' - end is at {(x_end, y_end)}')
            print(f' - length = {line_len} px')
            print(f' - angle = {line_ang:.2f} °')
            print(f' - gauge value = {pressure:.0f} bars')
            # draw detected line in green
            # cv2.line(flat_img, (x1, y1), (x2, y2), (0, 255, 0), 8)
            # draw normalized line in blue
            cv2.line(flat_img, (x_end, y_end), (x_center, y_center), (0, 0, 255), 8)

# show images
fig = plt.figure()
fig.add_subplot(131)
plt.title('original picture')
plt.imshow(origin_img)
fig.add_subplot(132)
plt.title('flatted image masked')
plt.imshow(flat_img_mask)
fig.add_subplot(133)
plt.title('needle position')
plt.imshow(flat_img)
plt.show()
