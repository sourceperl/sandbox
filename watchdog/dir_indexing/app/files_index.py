import logging
from pathlib import Path

from .sha256 import calculate_sha256

logger = logging.getLogger(__name__)


class FilesIndex:
    def __init__(self, watched_path: Path, index_path: Path, skip_patterns: list[str] = []) -> None:
        # args
        self.watched_path = watched_path
        self.index_path = index_path
        self.skip_patterns = skip_patterns
        # internal sha256 cache
        self._files_sha256_d = {}

    def _get_index_name(self, file_path: Path) -> str:
        return str(file_path.relative_to(self.watched_path))

    def add(self, file_path: Path, force: bool = False) -> bool:
        # allow only file
        if not file_path.is_file():
            return False
        # skip file which are not in the watched directory
        if not file_path.is_relative_to(self.watched_path):
            return False
        # exclude index file to prevent infinite loop
        if file_path.samefile(self.index_path):
            return False
        # skip file if any skip pattern match
        for pattern in self.skip_patterns:
            if file_path.match(pattern):
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
        logger.debug(f'compute sha256 for {file_path} ({short_hash})')
        # check if the file is not already well indexed (in the index with a good checksum)
        if self._files_sha256_d.get(index_name) == checksum:
            return False
        else:
            self._files_sha256_d[index_name] = checksum
            return True

    def delete(self, file_path: Path) -> bool:
        try:
            del self._files_sha256_d[self._get_index_name(file_path)]
            return True
        except KeyError:
            return False

    def index_all(self):
        """ Walks on watched directory, calculates SHA256 for all files and writes them to the index file. """
        # clean before populate cache
        self._files_sha256_d.clear()
        # add all files in the watched directory
        for file in self.watched_path.rglob('*'):
            self.add(file)
        # create or update index file
        self.sync()

    def sync(self):
        """ Transfer internal sha256 cache to a sorted index file. """
        try:
            with open(self.watched_path / self.index_path, 'w') as f:
                for file, sha256 in sorted(self._files_sha256_d.items()):
                    f.write(f'{sha256} {file}\n')
            logger.debug(f'index file "{self.index_path}" has been regenerated.')
        except Exception as e:
            logger.error(f'error writing to output file: {e}')
