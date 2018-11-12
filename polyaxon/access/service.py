from hestia.service_interface import Service, InvalidService

from django.conf import settings

from access.basic import owner, project
from access.entities import Entities
from scopes.manager import ScopeMappingManager
from scopes.roles.manager import RoleManager


class AccessService(Service):
    __all__ = ('setup', 'get_scope_mapping_for', 'has_object_permission', 'entities',)

    ENTITY_MAPPING = {
        Entities.OWNER: owner.has_object_permission,
        Entities.PROJECT: project.has_object_permission
    }

    def __init__(self):
        self.role_manager = None
        self.scope_mapping_manager = None

    @property
    def entities(self):
        return self.entities

    def get_scope_mapping_for(self, endpoint):
        self.scope_mapping_manager.get(endpoint=endpoint)

    def has_object_permission(self, entity, permission, request, view, obj):
        if entity not in self.entities.VALUES:
            raise InvalidService('Entity not support `{}`'.format(entity))

        return self.ENTITY_MAPPING[entity](permission=permission,
                                           request=request,
                                           view=view,
                                           obj=obj)

    def setup(self):
        super().setup()

        self.role_manager = RoleManager(config=settings.ROLES, default=settings.DEFAULT_ROLE)
        self.scope_mapping_manager = ScopeMappingManager(config=settings.SCOPE_ROLES)
        self._entities = Entities
