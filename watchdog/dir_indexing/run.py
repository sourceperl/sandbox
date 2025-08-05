import argparse
import sys

from app import main
from private_data import WATCHED_DIR

# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()

# main (don't index files like "_skip_file.txt")
sys.exit(main(watched_dir=WATCHED_DIR, skip_patterns=['_*'], debug=args.debug))
