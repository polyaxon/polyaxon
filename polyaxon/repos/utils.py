from repos.models import CodeReference


def assign_code_reference(instance):
    if not instance.project.has_code:
        return

    # Set the code reference to the experiment
    repo = instance.project.repo
    last_commit = repo.last_commit
    if last_commit:
        code_reference, _ = CodeReference.objects.get_or_create(repo=repo, commit=last_commit[0])
        instance.code_reference = code_reference

    return instance
