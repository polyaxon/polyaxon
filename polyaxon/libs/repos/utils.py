from db.models.repos import CodeReference


def get_project_latest_code_reference(project):
    if not project.has_code:
        return None

    # Set the code reference to the experiment
    repo = project.repo
    last_commit = repo.last_commit
    if not last_commit:
        return None

    code_reference, _ = CodeReference.objects.get_or_create(repo=repo, commit=last_commit[0])
    return code_reference


def get_latest_code_reference(instance):
    return get_project_latest_code_reference(instance.project)


def assign_code_reference(instance):
    code_reference = get_latest_code_reference(instance=instance)
    if code_reference:
        instance.code_reference = code_reference

    return instance
