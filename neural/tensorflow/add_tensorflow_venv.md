# On Raspberry Pi 4 with bullseye 64 bits


## Create a python virtual environment
```bash
# create
mkdir -p venv/tflow-2.9.0
python -m venv venv/tflow-2.9.0
# activate it (exit with deactivate command)
source venv/tflow-2.9.0/bin/activate
```

## Add packages to venv/tflow-2.9.0
```bash
# add packages
pip install Pillow numpy opencv-python
# add tensorflow wheel
pip install https://github.com/PINTO0309/Tensorflow-bin/releases/download/v2.9.0/tensorflow-2.9.0-cp39-none-linux_aarch64.whl
```

## Train a model with Teachable Machine

URL: https://teachablemachine.withgoogle.com/

Use it with scripts:
- "use_tm_model_img.py" for image source.
- "use_tm_model_cam.py" for USB camera source.
