# code from https://github.com/googlecreativelab/teachablemachine-community/

from os import chdir
from os.path import abspath, dirname
from keras.models import load_model
from PIL import Image, ImageOps
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

# predictions loop
for file in ['data/tm/test_1.png', 'data/tm/test_2.png']:
    # print filename
    print(f'start predict for file: {file}')

    # replace this with the path to your image
    image = Image.open(file).convert('RGB')

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # load the image into the array
    data[0] = normalized_image_array

    # predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # print prediction and confidence score
    print('Class:', class_name[2:], end='')
    print('Confidence Score:', confidence_score)
