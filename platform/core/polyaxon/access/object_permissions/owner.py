from rest_framework import permissions

from django.http import HttpRequest

from scopes.access import DEFAULT_ACCESS, OWNER_ACCESS, SUPERUSER_ACCESS, UNAUTHENTICATED_ACCESS


def has_object_permission(permission: permissions.BasePermission,
                          request: HttpRequest,
                          view,
                          obj: any) -> bool:
    user = request.user

    if not user or user.is_anonymous or not user.is_active:
        request.access = UNAUTHENTICATED_ACCESS
        return False

    if user.is_superuser or user.is_staff:
        request.access = SUPERUSER_ACCESS
        return True

    if obj.owner == user:
        request.access = OWNER_ACCESS
        return True

    request.access = DEFAULT_ACCESS
    return True
