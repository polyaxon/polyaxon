from collections import namedtuple

from django.utils.functional import cached_property


class RoleSpec(namedtuple("RoleSpec", "rank name desc scopes is_global")):

    @cached_property
    def id(self) -> str:
        return str.lower(self.name)

    def has_scope(self, scope) -> bool:
        return scope in self.scopes

    @classmethod
    def get_dummy(cls) -> 'RoleSpec':
        return cls(0, 'dummy', '', '', True)
