class Access(object):

    def __init__(self,
                 is_superuser=False,
                 is_owner=False,
                 public_only=True,
                 is_authenticated=True,
                 scopes=None,
                 permissions=None):
        self.is_superuser = is_superuser
        self.is_owner = is_owner
        self.is_authenticated = is_authenticated
        self.scopes = scopes or frozenset()
        self.permissions = permissions or frozenset()
        self.public_only = public_only

    def has_permission(self, permission):
        return permission in self.permissions

    def has_scope(self, scope):
        return scope in self.scopes


UNAUTHENTICATED_ACCESS = Access(is_authenticated=False)
DEFAULT_ACCESS = Access()
SUPERUSER_ACCESS = Access(is_superuser=True, public_only=False)
OWNER_ACCESS = Access(is_owner=True, public_only=False)
