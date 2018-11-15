from rest_framework.generics import get_object_or_404

import access

from api.endpoint.project import ProjectPermission, ProjectResourceEndpoint
from db.models.experiments import Experiment


class ExperimentEndpoint(ProjectResourceEndpoint):
    queryset = Experiment.objects
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('experiment_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('experiment',)
    lookup_url_kwarg = 'experiment_id'

    def _initialize_context(self):
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.experiment = self.get_object()


class ExperimentResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('experiment_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('experiment',)
    lookup_url_kwarg = 'experiment_id'

    def enrich_queryset(self, queryset):
        return queryset.filter(experiment=self.experiment)

    def _initialize_context(self):
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.experiment = get_object_or_404(Experiment,
                                            id=self.experiment_id,
                                            project=self.project)


class ExperimentResourcePermission(ProjectPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('ProjectResource')

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.experiment.project)


class ExperimentResourceEndpoint(ExperimentResourceListEndpoint):
    permission_classes = (ExperimentResourcePermission,)
    AUDITOR_EVENT_TYPES = None
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def _validate_context(self):
        #  pylint:disable=bad-super-call
        super(ExperimentResourceListEndpoint, self)._validate_context()
