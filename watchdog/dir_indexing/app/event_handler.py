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
    """Event handler that triggers the index generation function on file system changes.

    This class extends `watchdog`'s `FileSystemEventHandler` to listen for file
    creation, deletion, modification, and move events. It uses an instance of
    `FilesIndex` to manage an in-memory index of files and their SHA256 hashes,
    synchronizing the index to a file on each change.
    """

    def __init__(self, watched_path: Path, index_path: Path, files_index: FilesIndex):
        """Initializes the event handler with the necessary file paths and index object.

        Args:
            watched_path (Path): The root directory being watched for events.
            index_path (Path): The path to the index file itself. Events on
                               this file will be ignored to prevent infinite loops.
            files_index (FilesIndex): An instance of the FilesIndex class to
                                      manage file hashing and indexing.
        """
        super().__init__()
        # args
        self.watched_path = watched_path
        self.index_path = index_path
        self.files_index = files_index

    def on_any_event(self, event: FileSystemEvent):
        """Handles any file system event by updating the file index.

        This method is the primary entry point for all file system events. It
        first filters out directory events and events related to the index file
        itself. Based on the event type (`Created`, `Deleted`, `Modified`, `Moved`),
        it calls the corresponding method on the `FilesIndex` object to update the
        in-memory index. After each successful update, it triggers a
        synchronization to persist the changes to the index file. 

        This method also ensures that the index file is regenerated in case of accidental deletion.

        Args:
            event (FileSystemEvent): The event object containing information
                                     about the file system change.
        """
        # skip events for directories
        if event.is_directory:
            return
        # src_path as Path
        event_src_path = Path(event.src_path)
        # log unignored event message
        logger.debug(f'receive {event}')
        # trigger index generation on any change
        if isinstance(event, FileCreatedEvent):
            if self.files_index.add(event_src_path):
                logger.info(f'add file "{event_src_path.name}" to index')
                self.files_index.sync()
        elif isinstance(event, FileDeletedEvent):
            # deletion of the index file -> regenerate it
            if event_src_path.resolve() == self.index_path.resolve():
                logger.info(f'index file "{self.index_path.name}" removed: rebuild it from in-memory cache')
                self.files_index.sync()
            # other files process
            elif self.files_index.delete(event_src_path):
                logger.info(f'remove file "{event_src_path.name}" from index')
                self.files_index.sync()
        elif isinstance(event, FileModifiedEvent):
            if self.files_index.add(event_src_path, force=True):
                logger.info(f'update file "{event_src_path.name}" in index')
                self.files_index.sync()
        elif isinstance(event, FileMovedEvent):
            event_dest_path = Path(event.dest_path)
            if self.files_index.move(event_src_path, event_dest_path):
                logger.info(f'move file from "{event_src_path.name}" to "{event_dest_path.name}" in index')
                self.files_index.sync()
