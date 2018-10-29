from django.core.exceptions import ObjectDoesNotExist

from db.models.repos import CodeReference


def get_internal_code_reference(instance, commit=None):
    project = instance.project

    if not project.has_code:
        return None

    repo = project.repo

    if commit:
        try:
            return CodeReference.objects.get(repo=repo, commit=commit)
        except ObjectDoesNotExist:
            return None

    # If no commit is provided we get the last commit, and save new ref if not found
    last_commit = repo.last_commit
    if not last_commit:
        return None

    code_reference, _ = CodeReference.objects.get_or_create(repo=repo, commit=last_commit[0])
    return code_reference


def get_external_code_reference(git_url, commit=None):
    code_reference, _ = CodeReference.objects.get_or_create(git_url=git_url, commit=commit)
    return code_reference


def assign_code_reference(instance, commit=None):
    if instance.code_reference is not None or instance.specification is None:
        return
    build = instance.specification.build if instance.specification else None
    if not commit and build:
        commit = build.commit
    git_url = build.git if build and build.git else None
    if git_url:
        code_reference = get_external_code_reference(git_url=git_url, commit=commit)
    else:
        code_reference = get_internal_code_reference(instance=instance, commit=commit)
    if code_reference:
        instance.code_reference = code_reference

    return instance
