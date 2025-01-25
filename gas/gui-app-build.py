#!/usr/bin/env python

import os
import subprocess
import zipapp
from datetime import datetime
from pathlib import Path
from shutil import copytree


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
    if path.name == '.gitignore':
        return False
    return True


if __name__ == '__main__':
    # origin path
    origin_path = Path(os.path.dirname(os.path.realpath(__file__)))

    # source path
    src_path = Path(origin_path / 'gui-app')

    # build app_info.txt in archive
    build_app_info(to_path=Path(src_path / 'app_info.txt'), app_name='gas-gui')

    # copy the requirements
    copytree(src=origin_path / 'aga8', dst=src_path / 'aga8', dirs_exist_ok=True)
    copytree(src=origin_path / 'sgerg', dst=src_path / 'sgerg', dirs_exist_ok=True)

    # build zipapp
    zipapp.create_archive(
        source=src_path,
        target=origin_path / 'app.pyz',
        interpreter='/usr/bin/env python',
        filter=in_zip,
        compressed=True,
    )
