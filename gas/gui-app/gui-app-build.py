#!/usr/bin/env python

import os
import subprocess
import zipapp
from datetime import datetime
from pathlib import Path
from shutil import copytree

from app.const import APP_NAME

# some const
ZIP_FILE = 'app.pyz'


# get the last commit id from git command
def last_commit_id() -> str:
    return subprocess.check_output('git rev-parse HEAD'.split()).decode('ascii').strip()


# add a file with build infos to the zipapp
def build_app_info(to_path: Path, app_name: str):
    # build the content
    info_txt = ''
    info_txt += f'app name    : {app_name}\n'
    info_txt += f'build date  : {datetime.now().astimezone().isoformat()}\n'
    info_txt += f'last commit : {last_commit_id()}\n'
    # write it to file
    with open(to_path, 'w') as f:
        f.write(info_txt)


# archive build filter
def in_zip(path: Path) -> bool:
    # don't add the files or directories from the list to the zip file
    if path.name in [ZIP_FILE, '__pycache__', '.gitignore', os.path.basename(__file__)]:
        return False
    # also avoid to add files like 'package/__pycache__/*.pyc'
    for ancestor in path.parents:
        if ancestor.name == '__pycache__':
            return False
    return True


if __name__ == '__main__':
    # origin path
    origin_path = Path(os.path.dirname(os.path.realpath(__file__)))

    # build app_info.txt in archive
    build_app_info(to_path=Path(origin_path / 'app_info.txt'), app_name=APP_NAME)

    # copy the requirements
    copytree(src=origin_path / '../aga8/AGA8', dst=origin_path / 'AGA8', dirs_exist_ok=True)
    copytree(src=origin_path / '../sgerg/SGERG_88', dst=origin_path / 'SGERG_88', dirs_exist_ok=True)
    copytree(src=origin_path / '../iso_6976/ISO_6976', dst=origin_path / 'ISO_6976', dirs_exist_ok=True)
    copytree(src=origin_path / '../gerg_water/GERG_WATER', dst=origin_path / 'GERG_WATER', dirs_exist_ok=True)

    # build zipapp
    zipapp.create_archive(
        source=origin_path,
        target=origin_path / ZIP_FILE,
        interpreter='/usr/bin/env python',
        filter=in_zip,
        compressed=True,
    )
