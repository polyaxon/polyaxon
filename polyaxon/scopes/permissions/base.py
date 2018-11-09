from rest_framework import permissions


class PolyaxonPermission(permissions.BasePermission):
    """
    Polyaxon Base permission system.
    """

    def has_object_permission(self, request, view, obj):
        return False
