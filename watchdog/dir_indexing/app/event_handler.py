import logging
from pathlib import Path

from watchdog.events import (
    FileCreatedEvent,
    FileClosedEvent,
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
        # skip FileModifiedEvent (too verbose for large downloaded file)
        if isinstance(event, FileModifiedEvent):
            return
        # src_path as Path
        event_src_path = Path(event.src_path)
        # log unignored event message
        logger.debug(f'receive {event}')
        # event for index file ?
        if event_src_path.resolve() == self.index_path.resolve():
            # deletion of the index file -> regenerate it
            if isinstance(event, FileDeletedEvent):
                logger.info(f'index file "{self.index_path.name}" removed: rebuild it from in-memory cache')
                self.files_index.sync()
            return
        # trigger index generation on any change
        if isinstance(event, FileCreatedEvent):
            logger.info(f'file created "{event_src_path.name}"')
            if self.files_index.add(event_src_path):
                self.files_index.sync()
            return
        if isinstance(event, FileDeletedEvent):
            logger.info(f'file deleted "{event_src_path.name}"')
            if self.files_index.delete(event_src_path):
                self.files_index.sync()
            return
        if isinstance(event, FileClosedEvent):
            logger.info(f'file closed (probably updated) "{event_src_path.name}"')
            if self.files_index.add(event_src_path, force=True):
                self.files_index.sync()
            return
        if isinstance(event, FileMovedEvent):
            event_dest_path = Path(event.dest_path)
            logger.info(f'file moved from "{event_src_path.name}" to "{event_dest_path.name}"')
            if self.files_index.move(event_src_path, event_dest_path):
                self.files_index.sync()
            return
