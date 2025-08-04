import hashlib
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def calculate_sha256(file_path: Path) -> Optional[str]:
    """
    Calculates the SHA256 checksum of a file.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            # read and update hash in chunks to handle large files efficiently
            for byte_block in iter(lambda: f.read(4096), b''):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logger.error(f'error processing file {file_path}: {e}')
        return None
