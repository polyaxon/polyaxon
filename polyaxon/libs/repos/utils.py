from typing import Optional, Union

from django.core.exceptions import ObjectDoesNotExist

from db.models.repos import CodeReference


def _get_repo_code_reference(repo: 'Repo',
                             branch: str = None,
                             commit: str = None) -> Optional['CodeReference']:

    if commit:
        try:
            return CodeReference.objects.get(repo=repo,
                                             branch=branch,
                                             commit=commit)
        except ObjectDoesNotExist:
            return None

    # If no commit is provided we get the last commit, and save new ref if not found
    try:
        last_commit = repo.last_commit
    except ValueError:
        return None

    code_reference, _ = CodeReference.objects.get_or_create(repo=repo,
                                                            branch=branch,
                                                            commit=last_commit[0])
    return code_reference


def _get_external_repo_code_reference(repo: 'ExternalRepo',
                                      branch: str = None,
                                      commit: str = None) -> Optional['CodeReference']:
    from libs.repos import git

    def get_or_create(ref):
        code_references = CodeReference.objects.filter(external_repo=repo,
                                                       git_url=repo.git_url,
                                                       branch=branch,
                                                       commit=ref)
        if code_references.exists():
            return code_references.last()
        return CodeReference.objects.create(external_repo=repo,
                                            git_url=repo.git_url,
                                            branch=branch,
                                            commit=ref)

    # Fetch latest
    git.fetch(git_url=repo.git_clone_url, repo_path=repo.path, branch=branch, reset_remote=True)
    if commit:
        return get_or_create(ref=commit)

    # If no commit is provided we get the last commit, and save new ref if not found
    try:
        last_commit = repo.last_commit
    except ValueError:
        return None

    return get_or_create(ref=last_commit[0])


def get_code_reference(project: 'Project',
                       branch: str = None,
                       commit: str = None) -> Optional['CodeReference']:

    if not project.has_code:
        return None

    if project.has_external_repo:  # pylint:disable=no-else-return
        repo = project.external_repo
        return _get_external_repo_code_reference(repo=repo, branch=branch, commit=commit)
    else:
        repo = project.repo
        return _get_repo_code_reference(repo=repo, branch=branch, commit=commit)


RefModel = Union['Experiment',
                 'ExperimentGroup',
                 'Job',
                 'BuildJob',
                 'TensorboardJob',
                 'NotebookJob']


def assign_code_reference(instance: RefModel, branch: str = None, commit: str = None) -> RefModel:
    if instance.code_reference is not None or instance.specification is None:
        return instance
    build = instance.specification.build if instance.specification else None
    if not commit and build:
        commit = build.commit
    if not branch and build:
        branch = build.branch
    if not branch:
        branch = 'master'
    code_reference = get_code_reference(project=instance.project, branch=branch, commit=commit)
    if code_reference:
        instance.code_reference = code_reference

    return instance
