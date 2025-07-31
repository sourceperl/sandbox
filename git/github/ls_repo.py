#!/usr/bin/env python3

""" Lists repositories that the authenticated user has explicit permission (:read, :write, or :admin) to access.

https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-the-authenticated-user
"""

import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from private_data import GITHUB_TOKEN

url = f'https://api.github.com/user/repos'
all_repos = []
per_page = 100
page = 1

while True:
    query_string = urlencode({'type': 'owner', 'per_page': per_page, 'page': page})
    full_url = f'{url}?{query_string}'
    req = Request(full_url, headers={'Authorization': f'Bearer {GITHUB_TOKEN}',
                                     'Accept': 'application/vnd.github+json',
                                     'X-GitHub-Api-Version': '2022-11-28'})
    try:
        with urlopen(req) as response:
            status_code = response.getcode()
            if status_code == 200:
                repos = json.loads(response.read().decode('utf-8'))
                all_repos.extend(repos)
                # break the loop if no more repositories
                if len(repos) < per_page:
                    break
                # request next page
                page += 1
            else:
                print(f"Error: {status_code} - {response.read().decode('utf-8')}")
                break
    except URLError as e:
        print(f'Error: {e.reason}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

# show results
if all_repos:
    print(f'List of all repositories for this token (total: {len(all_repos)}):')
    for i, repo in enumerate(all_repos):
        msg = f"#{i+1:02d} - {repo['name']}"
        if repo['private']:
            msg += ' (private)'
        print(msg)
else:
    print('No repositories found or an error occurred.')
