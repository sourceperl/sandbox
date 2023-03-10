# original code from https://github.com/arunponnusamy/cvlib/

import time
import cv2
import cvlib as cvl


# open webcam
cam = cv2.VideoCapture(0)

# loop through frames
while True:
    # read 5 time to flush images buffer
    for _ in range(5):
        read_ok, img = cam.read()
    if not read_ok:
        break

    # apply object detection
    bbox_l, label_l, confidence_l = cvl.detect_common_objects(img, confidence=0.6, model='yolov3-tiny')

    # draw bounding box over detected objects
    img_with_box = cvl.object_detection.draw_bbox(img, bbox_l, label_l, confidence_l)

    # display output
    print(bbox_l, label_l, [round(x, 2) for x in confidence_l])
    cv2.imshow('real-time object detection', img_with_box)

    # exit on escape key press
    if cv2.waitKey(1) == 27:
        break

    # wait before next read/detect
    time.sleep(0.5)

# release resources
cam.release()
cv2.destroyAllWindows()
