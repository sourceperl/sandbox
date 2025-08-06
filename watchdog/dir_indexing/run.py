import argparse
import sys

from app import main
from private_data import WATCHED_DIR

# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()

# main (index files as "file.txt" but not as "_file.txt")
sys.exit(main(watched_dir=WATCHED_DIR, allow_patterns=['*.txt'], skip_patterns=['_*'], debug=args.debug))
