from collections import namedtuple

from django.utils.functional import cached_property


class RoleSpec(namedtuple("RoleSpec", "rank name desc scopes is_global")):

    @cached_property
    def id(self):
        return str.lower(self.name)

    def has_scope(self, scope):
        return scope in self.scopes
