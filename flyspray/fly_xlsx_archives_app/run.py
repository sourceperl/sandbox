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

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

logging.info("start of export task")
try:
    main(pub_path=pub_path)
except Exception as e:
    logging.error(f"error occurred during dashboard build: {e}")
logging.info("task done")
