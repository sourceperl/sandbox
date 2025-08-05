#!/usr/bin/env python3

"""
Monitor a specified directory for changes and automatically generate an index.txt file that contains the SHA256 
checksums of all files within that directory and its subdirectories. This index.txt file can be useful for verifying 
file integrity, tracking changes, or creating a simple manifest of a directory's contents.
"""

import logging
import time
from pathlib import Path

from watchdog.observers import Observer

from .event_handler import EventHandler
from .files_index import FilesIndex

logger = logging.getLogger(__name__)


def main(watched_dir: str, index_name: str = 'index.sha256', skip_patterns: list[str] = [], debug: bool = False) -> int:
    # change this to the path you want to watch
    watched_path = Path(watched_dir)
    # name of the output file
    index_file_path = watched_path / Path(index_name)

    # logging setup
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format='%(asctime)s - %(module)-16s - %(levelname)-8s - %(message)s', level=level)
    logging.getLogger('watchdog').setLevel(logging.WARNING)
    logger.info(f'app started (monitor directory "{watched_path}")')

    # check if the watched dir exists
    if not watched_path.is_dir():
        logger.error(f'error: directory "{watched_path}" not found.')
        return 1

    # generation of the index file at startup
    files_index = FilesIndex(watched_path, index_file_path, skip_patterns=skip_patterns)
    files_index.index_all()

    # set up the event handler
    event_handler = EventHandler(watched_path, index_file_path, files_index)

    # set up the observer (ignore sub-directories)
    observer = Observer()
    observer.schedule(event_handler=event_handler, path=watched_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    return 0
