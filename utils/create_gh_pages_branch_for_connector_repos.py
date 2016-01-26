"""
This script creates a gh-pages branch on each Github repository in the variable
CONNECTOR_REPOS.
"""

# The ecology-connector repo isn't included here because the repo is currently
# private.
CONNECTOR_REPOS = [
    'health-connector',
    'cognitive-science-connector',
    'literature-connector',
    'geospatial-connector',
    'history-connector',
    'smart-cities-connector',
    'ethics-connector',
]

import os
from subprocess import call, DEVNULL

GH_PAGES = 'gh-pages'

def call_and_print(*cmd):
    print(' '.join(cmd))
    return call(cmd)

def git(*cmd):
    return call_and_print(* (('git',) + cmd))

def add_gh_pages(repo):
    print(repo)
    print('-' * len(repo))

    git('clone', 'https://github.com/dsten/' + repo)

    os.chdir(repo)
    git('branch', GH_PAGES)
    git('checkout', GH_PAGES)
    git('push', 'origin', 'gh-pages')

    os.chdir(os.pardir)
    call_and_print('rm', '-rf', repo)

    print()

if __name__ == '__main__':
    for repo in CONNECTOR_REPOS:
        add_gh_pages(repo)
