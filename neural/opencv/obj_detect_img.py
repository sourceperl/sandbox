# original code from https://github.com/arunponnusamy/cvlib/

import argparse
import cv2
import cvlib as cvl


# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('image_file', help='image for detection')
args = parser.parse_args()

# open image
img = cv2.imread(args.image_file)

# apply object detection
bbox_l, label_l, confidence_l = cvl.detect_common_objects(img, confidence=0.6, model='yolov4-tiny')

# draw bounding box over detected objects
img_with_box = cvl.object_detection.draw_bbox(img, bbox_l, label_l, confidence_l)

# display output
print(bbox_l, label_l, [round(x, 2) for x in confidence_l])
cv2.imshow('object detection', img_with_box)

# exit on escape key press
cv2.waitKey()

# save output
cv2.imwrite('detect_out.jpg', img_with_box)

# release resources
cv2.destroyAllWindows()
