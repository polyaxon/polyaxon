from django.core.exceptions import ObjectDoesNotExist

from db.models.repos import CodeReference


def get_code_reference(instance, commit=None, external_repo=None):
    project = instance.project

    if external_repo:
        repo = external_repo
    elif project.has_code:
        repo = project.repo

    if not repo:
        return None

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


def assign_code_reference(instance, commit=None):
    if instance.code_reference is not None:
        return
    build = instance.specification.build if instance.specification else None
    if not commit and build:
        commit = build.commit
    external_repo = build.git if build and build.git else None
    code_reference = get_code_reference(instance=instance,
                                        commit=commit,
                                        external_repo=external_repo)
    if code_reference:
        instance.code_reference = code_reference

    return instance
