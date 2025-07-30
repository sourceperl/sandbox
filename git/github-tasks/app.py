#!/usr/bin/env python3

"""
Automate some periodic GitHub tasks like backing up the GitHub gist and repositories.


Before use this, add the github-backup tool (https://github.com/josegonzalez/python-github-backup):
    # add pipx tool
    sudo apt install pipx
    # install github-backup tool
    pipx install github-backup

Also use some Python libraries:
    sudo apt install python3-git python3-schedule
"""


import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

import schedule
from git import InvalidGitRepositoryError, NoSuchPathError
from git.repo.base import Repo

from private_data import BACKUP_PATH, GITHUB_TOKEN, GITHUB_USER

logger = logging.getLogger(__name__)


def merge_git_repo(repo_path: Path):
    try:
        # define git repo
        logger.debug(f'process repository "{repo_path}"')
        repo = Repo(repo_path)
        # skip bare repository
        if repo.bare:
            raise RuntimeError(f'repository at "{repo_path}" is bare, skip it')
        # check repo is clean
        if repo.is_dirty():
            raise RuntimeError(f'repository at "{repo_path}" has uncommitted changes -> check it manualy')
        # find current active branch on this repository
        active_branch = Repo(repo_path).active_branch
        # try to find the remote branch matching the active branch
        remote_branch = repo.remotes.origin.refs[active_branch.name]
        logger.debug(f'find remote "{remote_branch.name}" matching current active branch "{active_branch.name}"')
        # try to merge with the remote branch
        merge_result = repo.git.merge(remote_branch)
        logger.debug(f'{merge_result=}')
    except NoSuchPathError:
        logger.warning(f'"{repo_path}" is not a valid path')
    except InvalidGitRepositoryError:
        logger.warning(f'"{repo_path}" is not a git repository')
    except Exception as e:
        logger.warning(f'{e!r}')


def step1_backup():
    """ start github-backup tool in current BACKUP_PATH. """
    try:
        logger.info(f'run tool "github-backup"')
        start_time = time.monotonic()
        cmd = f'github-backup {GITHUB_USER} -t {GITHUB_TOKEN} --all --private --fork --gists -o {BACKUP_PATH}'
        r_code = subprocess.call(cmd, shell=True)
        end_time = time.monotonic()
        elapsed_time = round(end_time - start_time)
        logger.info(f'"github-backup" tool return code {r_code} after {elapsed_time} s')
    except Exception as e:
        logger.error(f'error occur: {e}')


def step2_merge():
    """ try to merge current git branch with add-hoc remote. """
    base_dir = Path(BACKUP_PATH)

    # repositories
    logger.info('try to merge repositories')
    for repo_path in base_dir.glob('repositories/*/repository/'):
        merge_git_repo(repo_path)
    # gists
    logger.info('try to merge gists')
    for repo_path in base_dir.glob('gists/*/repository/'):
        merge_git_repo(repo_path)


def github_job():
    step1_backup()
    step2_merge()


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
    parser.add_argument('-s', '--single-shot', action='store_true', help='run in single shot mode')
    args = parser.parse_args()

    # logging setup
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(asctime)s.%(msecs)03d: %(message)s',
                        datefmt="%Y-%m-%dT%H:%M:%S", stream=sys.stdout, level=level)
    logging.getLogger('schedule').level = logging.WARNING

    # run once and exit (single shot mode)
    if args.single_shot:
        logger.info('github-tasks started in single shot mode')
        github_job()
        exit()

    # run in daemon mode (schedule a run once a day)
    logger.info('github-taks daemon started')
    schedule.every().day.at('23:15').do(github_job)

    # main loop
    while True:
        schedule.run_pending()
        time.sleep(1.0)
