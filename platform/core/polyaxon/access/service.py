from typing import Any, Dict

from hestia.service_interface import InvalidService, Service

from django.conf import settings
from django.http import HttpRequest

from access.object_permissions import admin, owner, owner_or_read_only
from access.resources import Resources
from scopes.manager import ScopeMappingManager


class AccessService(Service):
    __all__ = ('get_scope_mapping_for', 'has_object_permission',)

    ENTITY_MAPPING = {
        Resources.ADMIN: admin.has_object_permission,
        Resources.OWNER: owner.has_object_permission,
        Resources.CLUSTER: owner.has_object_permission,
        Resources.NODE: owner.has_object_permission,
        Resources.CATALOG: owner_or_read_only.has_object_permission,
        Resources.PROJECT: owner_or_read_only.has_object_permission,
        Resources.PROJECT_SETTINGS: owner_or_read_only.has_object_permission,
    }

    def __init__(self):
        self._scope_mapping_manager = None

    def get_scope_mapping_for(self, endpoint: str) -> Dict:
        return self._scope_mapping_manager.get(endpoint=endpoint)

    def has_object_permission(self,
                              resource: str,
                              permission,
                              request: HttpRequest,
                              view,
                              obj: Any) -> bool:
        if resource not in Resources.VALUES:
            raise InvalidService('Resources not support `{}`'.format(resource))

        return self.ENTITY_MAPPING[resource](permission=permission,
                                             request=request,
                                             view=view,
                                             obj=obj)

    def setup(self) -> None:
        super().setup()

        self._scope_mapping_manager = ScopeMappingManager(config=settings.SCOPE_ROLES)
