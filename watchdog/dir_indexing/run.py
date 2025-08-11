#!/usr/bin/env python3

import argparse
import sys

from app import main

# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('watched_directory', type=str, help='path to the watched directory')
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()

# main (index files as "file.txt" but not as "_file.txt")
sys.exit(main(watched_dir=args.watched_directory, skip_patterns=['_*'], debug=args.debug))
