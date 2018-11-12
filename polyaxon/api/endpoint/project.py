import access
from access.entities import Entities

from api.endpoint.base import BaseEndpoint
from api.endpoint.owner import OwnerPermission


class ProjectPermission(OwnerPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('Project')

    def has_object_permission(self, request, view, obj):
        result = super().has_object_permission(request, view, obj.owner)
        if not result:
            return result

        return access.has_object_permission(
            entity=Entities.PROJECT,
            permission=ProjectPermission,
            request=request,
            view=view,
            obj=obj)


class ProjectEndpoint(BaseEndpoint):
    permission_classes = (ProjectPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name', 'project_name')
    lookup_field = 'name'
    lookup_url_kwarg = 'project_name'

    def filter_queryset(self, queryset):
        return queryset.filter(owner__name=self.owner_name)

    def _initialize_context(self):
        self.project = self.get_object()
        self.owner = self.project.owner
