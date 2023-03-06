# code from https://github.com/googlecreativelab/teachablemachine-community/

from os import chdir
from os.path import abspath, dirname
import cv2
from keras.models import load_model
import numpy as np


# chdir to script directory
chdir(dirname(abspath(__file__)))

# disable scientific notation for clarity
np.set_printoptions(suppress=True)

# load the model
model = load_model('models/tm/keras_model.h5', compile=False)

# load the labels
class_names = open('models/tm/labels.txt', 'r').readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# open video device (/dev/video0)
cam = cv2.VideoCapture(0)

# predictions loop
while True:
    # read image
    success, frame = cam.read()
    if not success:
        break

    # crop and resize image to 224x224
    h, w = frame.shape[:2]
    scare_size = min(h, w)
    m_h, m_w, m_s = h//2, w//2, scare_size//2
    crop_frame = frame[m_h-m_s:m_h+m_s, m_w-m_s:m_w+m_s]
    to_h, to_w = 224, 224
    image_array = cv2.resize(crop_frame, (to_h, to_w))

    # preview
    cv2.imshow('preview', image_array)

    # normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # load the image into the array
    data[0] = normalized_image_array

    # predicts the model
    prediction = model.predict(data, verbose=0)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # print prediction and confidence score
    print(f'class: {class_name[2:]:10s} (confidence: {100 * confidence_score:.2f} %)')

    # exit on escape key
    key = cv2.waitKey(10)
    if key == 27:
        break

# release resources
cam.release()
cv2.destroyAllWindows()
