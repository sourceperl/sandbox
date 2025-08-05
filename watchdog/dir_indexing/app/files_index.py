import logging
from pathlib import Path

from .sha256 import calculate_sha256

logger = logging.getLogger(__name__)


class FilesIndex:
    """
    Manages the indexing of files in a watched directory using SHA256 hashes.

    This class provides methods to add, delete, and move files within a watched
    directory, keeping an in-memory index of their SHA256 checksums. The index
    can be synchronized to a physical file in watched directory.
    """

    def __init__(self, watched_path: Path, index_path: Path, skip_patterns: list[str] = []) -> None:
        """
        Initializes the FilesIndex with the watched directory and index file path.

        Args:
            watched_path (Path): The root directory to be monitored for file changes.
            index_path (Path): The path to the file that will store the SHA256 index.
            skip_patterns (list[str]): A list of glob-style patterns to skip files.
                                       Defaults to an empty list.
        """
        # args
        self.watched_path = watched_path
        self.index_path = index_path
        self.skip_patterns = skip_patterns
        # internal sha256 cache
        self._files_sha256_d = {}

    def _get_index_name(self, file_path: Path) -> str:
        """
        Generates a relative path string to be used as a key in the index.

        Args:
            file_path (Path): The pathlib.Path object of the file.

        Returns:
            str: The file's path relative to the watched directory.
        """
        return str(file_path.relative_to(self.watched_path))

    def _is_skipped(self, file_path: Path) -> bool:
        for pattern in self.skip_patterns:
            if file_path.match(pattern):
                return True
        return False

    def add(self, file_path: Path, force: bool = False) -> bool:
        """
        Adds a file to the index, optionally forcing a hash re-computation.

        This method first performs several checks to determine if the file should be
        indexed. It skips files that are not within the watched directory, are the
        index file itself, or match a defined skip pattern.

        Args:
            file_path (Path): The pathlib.Path object for the file to add. It must be a path 
                              within the watched directory.
            force (bool): If True, re-computed the SHA256 hash even if the file is already present. 
                          Defaults to False.

        Returns:
            bool: True if the file was successfully added or updated in the index.
                  False if the file was skipped or an error occurred during hash computation.
        """
        # allow only file
        if not file_path.is_file():
            return False
        # skip file which are not in the watched directory
        if not file_path.is_relative_to(self.watched_path):
            return False
        # exclude index file to prevent infinite loop
        if file_path.exists() and self.index_path.exists() and file_path.samefile(self.index_path):
            return False
        # skip file if any skip pattern match
        if self._is_skipped(file_path):
            logger.debug(f'skip file "{file_path.name}"')
            return False
        # already in index ?
        index_name = self._get_index_name(file_path)
        if index_name in self._files_sha256_d and not force:
            return False
        # file_path to relative_path ("watched_dir_path/filename" -> "filename")
        checksum = calculate_sha256(file_path)
        if not checksum:
            return False
        # log short hash
        short_hash = checksum[:7]
        logger.debug(f'compute sha256 for "{file_path.name}" ({short_hash})')
        # check if the file is not already well indexed (in the index with a good checksum)
        if self._files_sha256_d.get(index_name) == checksum:
            return False
        else:
            self._files_sha256_d[index_name] = checksum
            return True

    def delete(self, file_path: Path) -> bool:
        """
        Deletes a file entry from the in-memory index.

        Args:
            file_path (Path): The pathlib.Path object of the file to remove.

        Returns:
            bool: True if the entry was successfully deleted. False if the
                  file was not found in the index.
        """
        try:
            del self._files_sha256_d[self._get_index_name(file_path)]
            return True
        except KeyError:
            return False

    def move(self, src_file_path: Path, dest_file_path: Path) -> bool:
        """Renames a file entry in the in-memory index.

        This method efficiently updates the index by renaming the key from the
        source path to the destination path without re-computing the hash.

        Args:
            src_file_path (Path): The pathlib.Path object of the file's old location.
            dest_file_path (Path): The pathlib.Path object of the file's new location.

        Returns:
            bool: True if the entry was successfully moved. False if the
                  source file was not found in the index.
        """
        src_index_name = self._get_index_name(src_file_path)
        dest_index_name = self._get_index_name(dest_file_path)
        # destination file match the skip patterns ?
        if self._is_skipped(dest_file_path):
            logger.debug(f'skip file "{dest_file_path.name}"')
            # delete source file from in-memory cache, lose destination file ignored
            try:
                self._files_sha256_d.pop(src_index_name)
                return True
            except KeyError:
                return False
        # add new destination file to in-memory cache
        logger.debug(f'add file "{dest_file_path.name}"')
        # attempt to efficiently rename the key in cache by reusing the hash from the source file entry
        try:
            self._files_sha256_d[dest_index_name] = self._files_sha256_d.pop(src_index_name)
            return True
        except KeyError:
            # do a full add since source file was not found in the cache
            return self.add(dest_file_path)

    def index_all(self):
        """
        Walks on the watched directory and adds all eligible files to the index.

        This method clears the current in-memory cache, recursively finds all
        files in the `watched_path`, calculates their SHA256 hashes, and adds them
        to the index. Finally, it synchronizes the index to the physical file.
        """
        # clean before populate cache
        self._files_sha256_d.clear()
        # add all files in the watched directory
        for file in self.watched_path.rglob('*'):
            self.add(file)
        # create or update index file
        self.sync()

    def sync(self):
        """
        Transfers the in-memory SHA256 cache to a sorted index file.

        The index file is written to the path specified in `self.index_path`.
        Each line in the file contains the SHA256 hash followed by the relative
        file path, separated by a space. The entries are sorted alphabetically
        by file path.
        """
        try:
            with open(self.watched_path / self.index_path, 'w') as f:
                for file, sha256 in sorted(self._files_sha256_d.items()):
                    f.write(f'{sha256} {file}\n')
            logger.info(f'index file "{self.index_path.name}" has been regenerated.')
        except Exception as e:
            logger.error(f'error writing to output file: {e}')
