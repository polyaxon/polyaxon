from rest_framework.generics import get_object_or_404

import auditor

from api.endpoint.project import ProjectEndpoint, ProjectResourceEndpoint
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.tensorboards import TensorboardJob
from scopes.authentication.utils import is_user


def get_target(experiment, group):
    if experiment:
        return 'experiment'
    elif group:
        return 'experiment_group'
    else:
        return 'project'


class TensorboardEndpoint(ProjectEndpoint):
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('tensorboard',)
    tensorboard_queryset = TensorboardJob.objects
    TENSORBOARD_AUDITOR_EVENT_TYPES = None

    def get_object(self):
        project = super().get_object()
        experiment_id = self.kwargs.get('experiment_id')
        group_id = self.kwargs.get('group_id')

        if experiment_id:
            tensorboard = get_object_or_404(self.tensorboard_queryset,
                                            project=project,
                                            experiment_id=experiment_id)
        elif group_id:
            tensorboard = get_object_or_404(self.tensorboard_queryset,
                                            project=project,
                                            experiment_group_id=group_id)
        else:
            tensorboard = get_object_or_404(self.tensorboard_queryset, project=project)

        if not self.TENSORBOARD_AUDITOR_EVENT_TYPES:
            return tensorboard

        target = get_target(experiment=experiment_id, group=group_id)
        method = self.request.method
        event_type = self.TENSORBOARD_AUDITOR_EVENT_TYPES.get(method)
        if method == 'GET' and event_type and is_user(self.request.user):
            auditor.record(event_type=event_type,
                           instance=tensorboard,
                           target=target,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        elif method == 'DELETE' and event_type and is_user(self.request.user):
            auditor.record(event_type=event_type,
                           instance=tensorboard,
                           target=target,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        return tensorboard

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        self.tensorboard = self.get_object()
        self.project = self.tensorboard.project
        self.owner = self.tensorboard.project.owner


class TensorboardResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('tensorboard', 'has_tensorboard')

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.tensorboard)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        project = self.project
        experiment_id = self.kwargs.get('experiment_id')
        group_id = self.kwargs.get('group_id')

        if experiment_id:
            experiment = get_object_or_404(Experiment, project=project, id=experiment_id)
            has_tensorboard = experiment.has_tensorboard
            tensorboard = experiment.tensorboard
        elif group_id:
            group = get_object_or_404(ExperimentGroup, project=project, id=group_id)
            has_tensorboard = group.has_tensorboard
            tensorboard = group.tensorboard
        else:
            has_tensorboard = project.has_tensorboard
            tensorboard = project.tensorboard

        self.tensorboard = tensorboard
        self.has_tensorboard = has_tensorboard
