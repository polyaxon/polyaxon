import logging

from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from projects.models import Project

logger = logging.getLogger("polyaxon.projects.permissions")


def has_project_permissions(user, project, request_method):
    """This logic is extracted here to be used also with Sanic api."""
    # Superusers and the creator is allowed to do everything
    if user.is_staff or project.user == user:
        return True

    # Other user
    return request_method in permissions.SAFE_METHODS and project.is_public


class IsProjectOwnerOrPublicReadOnly(permissions.BasePermission):
    """Custom permission to only allow owner to update/delete project.

    Other users can have read access if the project is public."""

    def has_object_permission(self, request, view, obj):
        # Check object type
        if not isinstance(obj, Project):
            logger.warning('Trying to check projects permission against %s',
                           obj.__class__.__name__)
            return False

        return has_project_permissions(user=request.user,
                                       project=obj,
                                       request_method=request.method)


class IsItemProjectOwnerOrPublicReadOnly(permissions.BasePermission):
    """Custom permission to only allow owner of project to update/delete project items.

    Other users can have read access if the project is public."""

    def has_object_permission(self, request, view, obj):
        # Check that obj has project attr
        if not hasattr(obj, 'project'):
            logger.warning('Trying to check project item permission against %s',
                           obj.__class__.__name__)
            return False

        return has_project_permissions(user=request.user,
                                       project=obj.project,
                                       request_method=request.method)


def check_access_project_item(view, request, project):
    permission = IsProjectOwnerOrPublicReadOnly()
    if not permission.has_object_permission(request, view, project):
        view.permission_denied(
            request, message=getattr(permission, 'message', None)
        )


def get_permissible_project(view):
    username = view.kwargs['username']
    project_name = view.kwargs['name']
    project = get_object_or_404(Project, name=project_name, user__username=username)

    # Check project permissions
    check_access_project_item(view=view, request=view.request, project=project)

    return project
