from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.project import ProjectPermission, ProjectResourcePermission


class PublicActivityPermission(ProjectPermission):
    """
    A Permission that checks allowed scopes,
    otherwise allows any user to interact with public projects.

    This is useful to allow to create bookmarks, searches, ...
    """
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.PUBLIC)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        result = super().has_object_permission(request, view, obj)
        return result or obj.is_public


class PublicResourceActivityPermission(ProjectResourcePermission):
    """
    A Permission that checks allowed scopes,
    otherwise allows any user to interact with public project's resources.

    This is useful to allow to create bookmarks, searches, ...
    """
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.PUBLIC)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        result = super().has_object_permission(request, view, obj)
        return result or obj.project.is_public
