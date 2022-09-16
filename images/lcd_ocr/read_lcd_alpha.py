#!/usr/bin/env python3

"""Decode content of an alphanumeric LCD."""

import cv2
import matplotlib.pyplot as plt
import numpy as np
# sudo apt install tesseract-ocr
# sudo pip3 install pytesseract
import pytesseract


# load image
origin_img = cv2.imread('img/lcd.jpg')
origin_img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2RGB)

# step 1: perspective change
# define quadrilateral corners to map to a rectangle (dst_box)
c1, c2 = [176, 110], [479, 192]
c4, c3 = [148, 168], [456, 265]
dst_box_w = max(c1[0], c2[0], c3[0], c4[0]) - min(c1[0], c2[0], c3[0], c4[0])
dst_box_h = max(c1[1], c2[1], c3[1], c4[1]) - min(c1[1], c2[1], c3[1], c4[1])
src_corners = np.float32([c1, c2, c3, c4])
dst_corners = np.float32([[0, 0], [dst_box_w - 1, 0], [dst_box_w - 1, dst_box_h - 1], [0, dst_box_h - 1]])
# apply change, create flatted image
matrix = cv2.getPerspectiveTransform(src_corners, dst_corners)
flat_img = cv2.warpPerspective(origin_img, matrix, (dst_box_w, dst_box_h), cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
# step 2: select by colors
# set lower and upper selected colors limits
low_color = np.array([0, 0, 0])
up_color = np.array([175, 175, 40])
flat_img_mask = cv2.inRange(flat_img, low_color, up_color)

# step 3: dilate for avoid holes in the characters
k = np.ones((2, 2), np.uint8)
flat_img_mask_dil = cv2.dilate(flat_img_mask, kernel=k, iterations=3)

# step 4: do OCR with tesseract tool
txt = pytesseract.image_to_string(flat_img_mask_dil)
txt = txt.strip()

# show results
fig = plt.figure()
fig.add_subplot('231')
plt.title('original picture')
plt.imshow(origin_img)
fig.add_subplot('232')
plt.title('flatted image')
plt.imshow(flat_img)
fig.add_subplot('233')
plt.title('mask image')
plt.imshow(flat_img_mask)
fig.add_subplot('234')
plt.title('dilate')
plt.imshow(flat_img_mask_dil)
fig.add_subplot('235')
plt.title('OCR return')
plt.xticks([])
plt.yticks([])
plt.text(0.5, 0.5, f'"{txt}"', horizontalalignment='center', verticalalignment='center')
plt.show()
