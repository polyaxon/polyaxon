from rest_framework import permissions

from django.http import HttpRequest

from scopes.access import DEFAULT_ACCESS


def has_object_permission(permission: permissions.BasePermission,
                          request: HttpRequest,
                          view,
                          obj: any) -> bool:
    # We check if the access type before continuing other checks
    if request.access.is_superuser or request.access.is_owner:
        return True

    # Other user
    if request.method in permissions.SAFE_METHODS and obj.is_public:
        request.access = DEFAULT_ACCESS
        return True

    return False
