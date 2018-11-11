import access
from api.endpoint.base import BaseEndpoint
from api.endpoint.owner import OwnerPermission


class ProjectPermission(OwnerPermission):
    ENTITY = 'Project'
    SCOPE_MAPPING = access.get_scope_mapping_for('Project')

    def has_object_permission(self, request, view, obj):
        result = super().has_object_permission(request, view, obj)
        if not result:
            return result

        return access.has_object_permission(
            entity=self.ENTITY,
            permission=self,
            request=request,
            view=view,
            obj=obj)


class ProjectEndpoint(BaseEndpoint):
    permission_classes = (ProjectPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner', 'project')
