#!/bin/bash

# Install the last release of tensorflow (test on RPI 5 debian 12.7 64 bits)

# abort on error
set -e

# tensorflow requirement: add development files for Hierarchical Data Format 5 (HDF5)
sudo apt install -y libhdf5-dev

# create a new venv
python -m venv venv
source venv/bin/activate

# add require packages
pip install -U pip
pip install pillow
pip install tensorflow
