from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from tensorflow import saved_model

# load model and labels
my_model = saved_model.load(export_dir='model.savedmodel')
class_names = open('labels.txt', 'r').readlines()


for image_name in map(str, sorted(Path('.').glob('*.jpg'))):
    # load and resizing the image to be at least 224x224 and then cropping from the center
    image = Image.open(image_name).convert('RGB')
    image = ImageOps.fit(image, size=(224, 224), method=Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_as_array = np.asarray(image)
    # normalize the image
    normalized_image_array = (image_as_array.astype(np.float32) / 127.5) - 1

    # load the image into the data array
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # run predicts model
    prediction = my_model(data)
    index = np.argmax(prediction)
    class_name = class_names[index].split()[1]
    confidence_score = round(float(prediction[0][index]) * 100, 2)

    # Print prediction and confidence score
    print(f'image "{image_name:24s}" is class "{class_name:8s}" conf score: {confidence_score:.02f} %')
