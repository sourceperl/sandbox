#!/usr/bin/env python3

"""QRcodes and barcodes USB camera scanner."""

import cv2
# sudo apt-get install libzbar0
# sudo pip3 install pyzbar
# see https://github.com/NaturalHistoryMuseum/pyzbar/
from pyzbar.pyzbar import decode

# open video device
cap = cv2.VideoCapture(0)
# set cam properties
# cap.set(cv2.CAP_PROP_BACKLIGHT, 0)

# display loop
while True:
    # read current image
    read_ok, img = cap.read()
    if not read_ok:
        break
    # transform image on need
    # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    # search for qrcodes or barcodes in image
    # grayscale seems to improve detection
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    codes_l = decode(img_gray)
    # format msg if code(s) available
    msg = ''
    if codes_l:
        for code in codes_l:
            msg += f'{code.type} at pos ({code.rect.left},{code.rect.top}): data={code.data}\n'
            cv2.rectangle(img, color=(0, 255, 0), thickness=2,
                          pt1=(code.rect.left, code.rect.top),
                          pt2=(code.rect.left + code.rect.width, code.rect.top + code.rect.height), )
            # print(f'RAW :{code}')
    print(msg)
    # add text overlay to image
    for index, line in enumerate(msg.split('\n')):
        at_pos = (30, 30 + 30 * index)
        cv2.putText(img, text=line, org=at_pos, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5, color=(0, 255, 0), thickness=1)
    # display result
    cv2.imshow('view', img)
    # exit on escape key
    key = cv2.waitKey(10)
    if key == 27:
        break

# some cleanup on exit
cap.release()
cv2.destroyAllWindows()
