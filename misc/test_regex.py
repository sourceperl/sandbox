#!/usr/bin/env python3

""" Test of regex.

- just pass string(s) as args on command line to test it.
"""

from pprint import pprint
import re
import sys


for test_str in sys.argv[1:]:
    print(f'test "{test_str}"')
    result = re.search(r'^(?!__.*)(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)(?:{(?P<labels>[^}]*)})?$', test_str)

    if result:
        print(f'\tfind name: {result.group("name")}')
        print(f'\tfind labels: {result.group("labels")}')
    else:
        print('no match')
    print('')
