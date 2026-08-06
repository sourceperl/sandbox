#!/usr/bin/env python3

"""
Export data from flyspray to xlsx dashboards using SQLAlchemy ORM.
"""

import logging
from pathlib import Path

from app import main

# define path to outputs dir
base_dir = Path(__file__).resolve().parent
pub_path = base_dir / 'outputs'

# global log conf: sets a default format and level for all loggers in this application
logging.basicConfig(format='%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s', level=logging.INFO)

logging.info("start of export task")
main(pub_path=pub_path)
logging.info("task done")
