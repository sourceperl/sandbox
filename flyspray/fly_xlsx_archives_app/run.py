#!/usr/bin/env python3

"""
Export data from flyspray to xlsx dashboards using SQLAlchemy ORM.
"""

import argparse
import logging
from pathlib import Path

from app import build_excel_reports, rename_attachments

if __name__ == '__main__':
    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rename', action='store_true', help='rename attachements')
    args = parser.parse_args()

    # define path to outputs dir
    base_dir = Path(__file__).resolve().parent
    pub_path = base_dir / 'outputs'

    # global log conf: sets a default format and level for all loggers in this application
    logging.basicConfig(format='%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s', level=logging.INFO)

    if args.rename:
        logging.info("start attachments rename task")
        rename_attachments(pub_path=pub_path)
        logging.info("task done")
    else:
        logging.info("start build excel reports task")
        build_excel_reports(pub_path=pub_path)
        logging.info("task done")
