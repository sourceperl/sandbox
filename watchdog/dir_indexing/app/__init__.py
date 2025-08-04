#!/usr/bin/env python3

"""
Monitor a specified directory for changes and automatically generate an index.txt file that contains the SHA256 
checksums of all files within that directory and its subdirectories. This index.txt file can be useful for verifying 
file integrity, tracking changes, or creating a simple manifest of a directory's contents.
"""

import logging
import time
from pathlib import Path
from typing import Optional

from watchdog.events import (
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer

from .sha256 import calculate_sha256

logger = logging.getLogger(__name__)


class FilesIndex:
    def __init__(self, watched_path: Path, index_path: Path) -> None:
        # args
        self.watched_path = watched_path
        self.index_path = index_path
        # internal sha256 cache
        self._files_sha256_d = {}
    
    def add_file(self, file_path: Path):
        # allow only file
        if not file_path.is_file():
            return
        # exclude index file to prevent infinite loop
        if file_path.samefile(self.index_path):
            return
        # file_path to relative_path ("watched_dir_path/filename" -> "filename")
        relative_path = file_path.relative_to(self.watched_path)
        checksum = calculate_sha256(file_path)
        if checksum:
            logger.debug(f'compute sha256 for {file_path} ({checksum[:10]})')
            self._files_sha256_d[relative_path.name] = checksum

    def init(self):
        """ Walks on watched directory, calculates SHA256 for all files and writes them to the index file. """
        # clean before populate cache
        self._files_sha256_d.clear()
        # add all files in the watched directory
        for file in self.watched_path.rglob('*'):
            self.add_file(file)
        # create or update index file
        self._build_index()

    def _build_index(self):
        """ Transfer internal sha256 cache to a sorted index file. """
        try:
            with open(self.watched_path / self.index_path, 'w') as f:
                for file, sha256 in sorted(self._files_sha256_d.items()):
                    f.write(f'{sha256} {file}\n')
            logger.debug(f'index file "{self.index_path}" has been updated.')
        except Exception as e:
            logger.error(f'error writing to output file: {e}')


class EventHandler(FileSystemEventHandler):
    """
    Event handler that triggers the index generation function on changes.
    """

    def __init__(self, dir_path: Path, index_path: Path, files_index: FilesIndex):
        super().__init__()
        # args
        self.dir_path = dir_path
        self.index_path = index_path
        self.files_index = files_index

    def on_any_event(self, event: FileSystemEvent):
        # skip events for directories
        if event.is_directory:
            return
        # skip events for the index file itself
        event_src_path = Path(event.src_path)
        if event_src_path.exists():
            if event_src_path.samefile(self.index_path):
                return
        # log unignored event message
        logger.debug(f'receive event {event}')
        # trigger index generation on any change
        if isinstance(event, (FileCreatedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent)):
            logger.info(f'change detected -> re-generating {self.index_path}')
            self.files_index.init()


def main(watched_dir: str, debug: bool = False) -> int:
    # change this to the path you want to watch
    watched_path = Path(watched_dir)
    # name of the output file
    index_file_path = watched_path / Path('index.sha256')

    # logging setup
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format='%(asctime)s - %(module)-12s - %(levelname)-8s - %(message)s', level=level)
    logging.getLogger('watchdog').setLevel(logging.WARNING)
    logger.info(f'app started (monitor directory "{watched_path}")')

    # check if the watched dir exists
    if not watched_path.is_dir():
        logger.error(f'error: directory "{watched_path}" not found.')
        return 1

    # generation of the index file at startup
    files_index = FilesIndex(watched_path, index_file_path)
    files_index.init()

    # set up the observer
    event_handler = EventHandler(watched_path, index_file_path, files_index)
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
