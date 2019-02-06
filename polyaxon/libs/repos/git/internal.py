import logging

_logger = logging.getLogger('polyaxon.repos.git')


def set_git_repo(repo: 'Repo') -> str:
    from libs.repos.git import ensure_repo_paths, get_git_repo

    # Ensure paths
    ensure_repo_paths(repo=repo)

    # Create a new repo
    get_git_repo(repo_path=repo.path, init=True)
    return repo.path
