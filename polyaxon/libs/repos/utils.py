from django.core.exceptions import ObjectDoesNotExist

from db.models.repos import CodeReference


def get_project_code_reference(project, commit=None):
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


def get_code_reference(instance, commit):
    return get_project_code_reference(instance.project, commit=commit)


def assign_code_reference(instance, commit=None):
    if not commit and instance.specification and instance.specification.build:
        commit = instance.specification.build.commit
    code_reference = get_code_reference(instance=instance, commit=commit)
    if code_reference:
        instance.code_reference = code_reference

    return instance
