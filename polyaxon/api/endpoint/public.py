import access
from api.endpoint.project import ProjectPermission


class PublicActivityPermission(ProjectPermission):
    """
    A Permission that checks allowed scopes,
    otherwise allows any user to interact with public repos.

    This is useful to allow to create bookmarks, searches, ...
    """
    SCOPE_MAPPING = access.get_scope_mapping_for('PublicInteraction')

    def has_object_permission(self, request, view, obj):
        result = super().has_object_permission(request, view, obj)
        return result or obj.is_public
