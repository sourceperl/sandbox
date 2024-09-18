#!/usr/bin/env python3

""" A custom IPython base environment. """

import sys

import matplotlib.pyplot as plt
import numpy as np
from IPython import embed

# init modbus client
try:
    # start in interractive mode
    sys.exit(embed(banner1='My custom IPython\n',
                   banner2='', exit_msg='Goodbye'))
except ValueError as e:
    print(e)
