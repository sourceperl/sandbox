import logging
from pathlib import Path

from watchdog.events import (
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEvent,
    FileSystemEventHandler,
)

from .files_index import FilesIndex

logger = logging.getLogger(__name__)


class EventHandler(FileSystemEventHandler):
    """
    Event handler that triggers the index generation function on changes.
    """

    def __init__(self, watched_path: Path, index_path: Path, files_index: FilesIndex):
        super().__init__()
        # args
        self.watched_path = watched_path
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
        logger.debug(f'receive {event}')
        # trigger index generation on any change
        if isinstance(event, FileCreatedEvent):
            if self.files_index.add(Path(event.src_path)):
                logger.info(f'add file {event.src_path} to index')
                self.files_index.sync()
        elif isinstance(event, FileDeletedEvent):
            if self.files_index.delete(Path(event.src_path)):
                logger.info(f'remove file {event.src_path} from index')
                self.files_index.sync()
        elif isinstance(event, FileModifiedEvent):
            if self.files_index.add(Path(event.src_path), force=True):
                logger.info(f'update file {event.src_path} in index')
                self.files_index.sync()
        elif isinstance(event, FileMovedEvent):
            self.files_index.add(Path(event.dest_path), force=True)
            self.files_index.delete(Path(event.src_path))
            logger.info(f'move file from {event.src_path} to {event.dest_path} in index')
            self.files_index.sync()
