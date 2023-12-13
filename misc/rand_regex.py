#!/usr/bin/env python3

""" Generate some random strings to check the strength of the regular expression. """

from datetime import datetime
import re
import random
import string


# some init
custom_chars = string.ascii_lowercase + '{}"=_'
pattern_metric = re.compile(r'(?!__.*)(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)(?:{(?P<labels>.*?)})?')
pattern_label = re.compile(r'(?:(?!__.*)[a-zA-Z_][a-zA-Z0-9_]*=\"[^\"]*\",?)+')

# main loop
while True:
    # build random string
    random_str = ''.join(random.choice(custom_chars) for _ in range(10))
    # test it
    match_metric = pattern_metric.fullmatch(random_str)
    if match_metric:
        labels_str = match_metric.group('labels')
        if labels_str:
            if pattern_label.fullmatch(labels_str):
                print(f'{datetime.now().isoformat()} test ok for: {random_str}')
