#!/usr/bin/env bash


# some consts
VENV_NAME="tflow-2.9.0"
VENV_DIR="${HOME}/.virtualenvs"
ARCH=$(uname -m)
PY_VER="39"

# create python virtual environment
mkdir -p ${VENV_DIR}
python -m venv ${VENV_DIR}/${VENV_NAME}
# activate it (exit with deactivate command)
source ${VENV_DIR}/${VENV_NAME}/bin/activate
# add packages
pip install Pillow numpy opencv-python cvlib
# add tensorflow wheel
pip install https://github.com/PINTO0309/Tensorflow-bin/releases/download/v2.9.0/tensorflow-2.9.0-cp${PY_VER}-none-linux_${ARCH}.whl
