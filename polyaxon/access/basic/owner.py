from scopes.access import DEFAULT_ACCESS, SUPERUSER_ACCESS, OWNER_ACCESS


def has_object_permission(permission, request, view, obj):
    user = request.user

    if not user or user.is_anonymous() or not user.is_active:
        request.access = DEFAULT_ACCESS
        return False

    if user.is_staff:
        request.access = SUPERUSER_ACCESS
        return True

    if obj == user:
        request.access = OWNER_ACCESS
        return True

    request.access = DEFAULT_ACCESS
    return True
