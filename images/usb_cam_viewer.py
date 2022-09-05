#!/usr/bin/env python3

"""Simple video device viewer."""

import cv2


# open video device
cap = cv2.VideoCapture(0)
# set camera properties
# cap.set(cv2.CAP_PROP_BACKLIGHT, 0)

# display loop
while True:
    # read and display current image
    success, frame = cap.read()
    if not success:
        break
    # show image with rotate
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('preview', frame)
    # exit on escape key
    key = cv2.waitKey(10)
    if key == 27:
        break

# some cleanup on exit
cap.release()
cv2.destroyAllWindows()
