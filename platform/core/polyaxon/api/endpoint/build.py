from rest_framework.generics import get_object_or_404

from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.project import ProjectPermission, ProjectResourceEndpoint
from db.models.build_jobs import BuildJob


class BuildEndpoint(ProjectResourceEndpoint):
    queryset = BuildJob.objects
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('build_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('build',)
    lookup_url_kwarg = 'build_id'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.build = self.get_object()


class BuildResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('build_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('build',)
    lookup_url_kwarg = 'build'

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.build)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.build = get_object_or_404(BuildJob,
                                       id=self.build_id,
                                       project=self.project)


class BuildResourcePermission(ProjectPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.PROJECT_RESOURCE)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        return super().has_object_permission(request, view, obj.job.project)


class BuildResourceEndpoint(BuildResourceListEndpoint):
    permission_classes = (BuildResourcePermission,)
    AUDITOR_EVENT_TYPES = None
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
