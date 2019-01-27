from rest_framework.generics import get_object_or_404

from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.experiment import ExperimentResourceEndpoint, ExperimentResourcePermission
from db.models.experiment_jobs import ExperimentJob


class ExperimentJobEndpoint(ExperimentResourceEndpoint):
    queryset = ExperimentJob.objects
    CONTEXT_KEYS = ExperimentResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ExperimentResourceEndpoint.CONTEXT_OBJECTS + ('job',)
    lookup_url_kwarg = 'job_id'

    def _initialize_context(self):
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.job = self.get_object()


class ExperimentJobResourceListEndpoint(ExperimentResourceEndpoint):
    CONTEXT_KEYS = ExperimentResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ExperimentResourceEndpoint.CONTEXT_OBJECTS + ('job',)
    lookup_url_kwarg = 'job_id'

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.job)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.job = get_object_or_404(ExperimentJob,
                                     id=self.job_id,
                                     experiment=self.experiment)


class ExperimentJobResourcePermission(ExperimentResourcePermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.PROJECT_RESOURCE)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        return super().has_object_permission(request, view, obj.job)


class ExperimentJobResourceEndpoint(ExperimentJobResourceListEndpoint):
    permission_classes = (ExperimentJobResourcePermission,)
    AUDITOR_EVENT_TYPES = None
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
