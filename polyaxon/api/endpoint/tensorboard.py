from rest_framework.generics import get_object_or_404

from api.endpoint.project import ProjectResourceEndpoint
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.tensorboards import TensorboardJob


def get_target(experiment, group):
    if experiment:
        return 'experiment'
    elif group:
        return 'experiment_group'
    return 'project'


class TensorboardEndpoint(ProjectResourceEndpoint):
    queryset = TensorboardJob.objects
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('tensorboard',)
    lookup_url_kwarg = 'job_id'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.tensorboard = self.get_object()


class ProjectTensorboardEndpoint(ProjectResourceEndpoint):
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


class TensorboardResourceListEndpoint(ProjectResourceEndpoint):
    CONTEXT_KEYS = ProjectResourceEndpoint.CONTEXT_KEYS + ('job_id',)
    CONTEXT_OBJECTS = ProjectResourceEndpoint.CONTEXT_OBJECTS + ('tensorboard',)
    lookup_url_kwarg = 'job_id'

    def enrich_queryset(self, queryset):
        return queryset.filter(job=self.tensorboard)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.tensorboard = get_object_or_404(TensorboardJob,
                                          id=self.job_id,
                                          project=self.project)
