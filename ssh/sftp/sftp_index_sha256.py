import re
from pathlib import Path
from typing import Dict, Union

from paramiko import RejectPolicy, SSHClient
from private_data_2 import HOSTNAME, PORT, USER


class MySFTP:
    """
    A class to manage SFTP operations over an SSH connection, with a focus on sha256 file index mangement.
    """

    # regex to match lines like "64_char_sha256_hash  filename"
    SHA_PATTERN = re.compile(r'([0-9a-fA-F]{64})\s+(.+)')

    def __init__(self, ssh: SSHClient, base_dir: Union[str, Path] = '') -> None:
        # args
        self.ssh = ssh
        self.base_dir = Path(base_dir)
        # open SFTP session
        self.sftp = ssh.open_sftp()

    def _real_path(self, filename: Union[str, Path]) -> str:
        """
        Constructs the full remote path by joining base_dir and filename.
        Ensures the path uses forward slashes.

        Args:
            filename (Union[str, Path]): The filename or relative path

        Returns:
            str: The absolute path on the remote SFTP server, with forward slashes
        """
        # pathlib handles concatenation correctly, then ensure forward slashes
        return str((self.base_dir / filename).as_posix())

    def file_as_bytes(self, remote_filename: Union[str, Path]) -> bytes:
        """
        Reads a remote file and returns its content as bytes.

        Args:
            remote_filename (Union[str, Path]): The name of the remote file

        Returns:
            bytes: The content of the file

        Raises:
            FileNotFoundError: if the remote file does not exist
        """
        remote_full_path = self._real_path(remote_filename)
        try:
            # Access self.sftp via the property, which ensures it's open
            with self.sftp.open(remote_full_path, mode='rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f'remote file "{remote_full_path}" not found')

    def index_as_dict(self, index_filename: Union[str, Path] = 'index.sha256') -> dict:
        """
        Reads a remote SHA256 index file and parses its contents into a dictionary.

        Args:
            index_filename (Union[str, Path]): The name of the SHA256 index file. Defaults to 'index.sha256'

        Returns:
            Dict[str, str]: A dictionary where keys are filenames and values are
                            their corresponding SHA256 checksums (lowercase)

        Raises:
            FileNotFoundError: if the remote index file does not exist
            UnicodeDecodeError: if the index file content cannot be decoded with UTF-8
        """
        sha256_d: Dict[str, str] = {}

        raw_index_bytes = self.file_as_bytes(index_filename)

        for line in raw_index_bytes.decode('utf-8').splitlines():
            # regex to match lines like "sha_hash filename"
            match = self.SHA_PATTERN.match(line.strip())
            if match:
                sha_hash, filename = match.groups()
                sha256_d[filename] = sha_hash.lower()
        return sha256_d

    def close(self):
        self.sftp.close()


# create SSH client
ssh = SSHClient()

# accept only known hosts (production environment)
ssh.set_missing_host_key_policy(RejectPolicy())
# first connect with ssh cli to update the system known_hosts file
ssh.load_system_host_keys()

# connect to remote server
ssh.connect(hostname=HOSTNAME, port=PORT, username=USER)

# init SFTP session
sftp = MySFTP(ssh, base_dir='carousel-img')

# display the file in the index with a preview of the contents
for filename, sha256 in sftp.index_as_dict().items():
    raw_content = sftp.file_as_bytes(filename)
    head = raw_content[:20]
    print(f'{filename:>16s} ({sha256[:7]}) {head=}')

# close connections
sftp.close()
ssh.close()
