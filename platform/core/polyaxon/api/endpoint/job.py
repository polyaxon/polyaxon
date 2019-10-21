from rest_framework.generics import get_object_or_404

from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.project import ProjectPermission, ProjectResourceEndpoint
from db.models.jobs import Job


class JobEndpoint(ProjectResourceEndpoint):
    queryset = Job.objects
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('job',)
    lookup_url_kwarg = 'job_id'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.job = self.get_object()


class JobResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('job',)
    lookup_url_kwarg = 'job'

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.job)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.job = get_object_or_404(Job,
                                     id=self.job_id,
                                     project=self.project)


class JobResourcePermission(ProjectPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.PROJECT_RESOURCE)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        return super().has_object_permission(request, view, obj.job.project)


class JobResourceEndpoint(JobResourceListEndpoint):
    permission_classes = (JobResourcePermission,)
    AUDITOR_EVENT_TYPES = None
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
