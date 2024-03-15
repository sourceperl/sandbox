#!/bin/bash

# bash script to build a new python venv

# global vars
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
ENV_DIR="${SCRIPT_DIR}/venv"

# check if already exist
if [ -d "$ENV_DIR" ]; then
    echo "virtual environment '$ENV_DIR' already exist, exit."
    exit 1
fi

# init a new one
if python3 -m venv "${ENV_DIR}";
then 
    echo "init new virtual environment in '${ENV_DIR}' OK"
else
    echo "an error occur during virtual environment init, exit"
    exit 2
fi

# activate it
if source "${ENV_DIR}/bin/activate";
then 
    echo "activation of new virtual environment OK"
else
    echo "an error occur during virtual environment activation, exit"
    exit 3
fi

# add some package(s) to venv
echo "add required packages to the new virtual environment"
pip install -U pip
pip install -r "${SCRIPT_DIR}/requirements.txt"
