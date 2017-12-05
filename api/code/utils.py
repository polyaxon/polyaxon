import os

from django.conf import settings
from git import Repo


def get_repos(user):
    user_repos_root = os.path.join(settings.REPOS_ROOT, user)
    repos = [get_repo(os.path.join(user, dir)) for dir in os.listdir(user_repos_root)]
    return [repo for repo in repos if not (repo is None)]


def get_repo(repo_path):
    if os.path.isdir(repo_path):
        try:
            return Repo(repo_path)
        except Exception:
            pass
    return None


def get_commit(name, commit):
    repo = get_repo(name)
    commit = repo.commit(commit)
    return commit


def archive_repo(repo, repo_name):
    with open(os.path.join(settings.REPOS_ARCHIVE_ROOT, '{}.tar'.format(repo_name)), 'wb') as fp:
        repo.archive(fp)
