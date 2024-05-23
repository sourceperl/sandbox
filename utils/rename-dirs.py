#!/usr/bin/env python3

""" Rename directories in current directory. """

import os
from os import path


# some functions
def upper_rate(text: str) -> float:
    total_chars = len(text)
    if total_chars > 0:
        upper_chars = sum(1 for c in text if c.isupper())
        return upper_chars / total_chars
    else:
        return 0.0


# main app (exit with ctrl-c)
try:
    # current path is base directory
    base_dir = os.getcwd()

    for entry in os.listdir(base_dir):
        # skip if it's not a directory
        if not path.isdir(entry):
            continue
        # already in the correct form
        if upper_rate(entry) < 0.5:
            continue
        # rename directory
        cur_dir = entry
        new_dir = cur_dir.strip().title()
        tokens_l = new_dir.split()
        if tokens_l and tokens_l[-1].upper() in ('DP', 'PRED'):
            tokens_l[-1] = tokens_l[-1].upper()
        new_dir = ' '.join(tokens_l)
        # confirm operation
        confirm_str = input(f'rename directory "{cur_dir}" to "{new_dir}" [(y)es/(n)o] ?')
        if confirm_str in ('Y', 'y'):
            print(f'do "{cur_dir}" -> "{new_dir}"')
            os.rename(cur_dir, new_dir)
except KeyboardInterrupt:
    pass
