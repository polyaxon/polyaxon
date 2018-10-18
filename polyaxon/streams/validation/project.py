from db.models.projects import Project
from libs.permissions.projects import has_project_permissions


def validate_project(request, username, project_name):
    try:
        project = Project.objects.get(name=project_name, user__username=username)
    except Project.DoesNotExist:
        return None, 'Project was not found'
    if not has_project_permissions(request.app.user, project, 'GET'):
        return None, "You don't have access to this project"
    return project, None
