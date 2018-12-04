from rest_framework import permissions


def has_object_permission(permission, request, view, obj):
    # We check if the access type before continuing other checks
    if request.access.is_superuser or request.access.is_owner:
        return True

    # Other user
    return request.method in permissions.SAFE_METHODS and obj.is_public
