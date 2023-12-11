""" Test of regex. 

- just pass string(s) as args on command line to test it.
"""

import re
import sys


for test_str in sys.argv[1:]:
    print(f'"{test_str}"')
    result = re.search(r'^(?!.*__.*)([a-zA-Z_:][a-zA-Z0-9_:]*)(?:\{([a-zA-Z0-9,\=\"]*)\})*', test_str)

    if result:
        re_groups = result.groups()
        print(f'find groups: {re_groups}')
    else:
        print('no match')
    print('')
