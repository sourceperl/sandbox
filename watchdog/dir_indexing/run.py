import argparse
import sys

from app import main
from private_data import WATCHED_DIR

# parse command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()

# main
sys.exit(main(watched_dir=WATCHED_DIR, debug=args.debug))
