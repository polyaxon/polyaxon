from scopes.exceptions import SuperuserRequired
from scopes.permissions.base import PolyaxonPermission


class SuperuserPermission(PolyaxonPermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.is_superuser:
            raise SuperuserRequired
        return False

    def has_object_permission(self, request, view, obj):
        return True
