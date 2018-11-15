from rest_framework.generics import get_object_or_404

import access

from api.endpoint.project import ProjectPermission, ProjectResourceEndpoint
from db.models.experiment_groups import ExperimentGroup


class ExperimentGroupEndpoint(ProjectResourceEndpoint):
    queryset = ExperimentGroup.objects
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('group_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('group',)
    lookup_url_kwarg = 'group_id'

    def _initialize_context(self):
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.group = self.get_object()


class ExperimentGroupResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('group_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('group',)
    lookup_url_kwarg = 'group_id'

    def enrich_queryset(self, queryset):
        return queryset.filter(experiment_group=self.group)

    def _initialize_context(self):
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.group = get_object_or_404(ExperimentGroup,
                                       id=self.group_id,
                                       project=self.project)


class ExperimentGroupResourcePermission(ProjectPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('ProjectResource')

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj.experiment_group.project)


class ExperimentGroupResourceEndpoint(ExperimentGroupResourceListEndpoint):
    permission_classes = (ExperimentGroupResourcePermission,)
    AUDITOR_EVENT_TYPES = None
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def _validate_context(self):
        #  pylint:disable=bad-super-call
        super(ExperimentGroupResourceListEndpoint, self)._validate_context()
