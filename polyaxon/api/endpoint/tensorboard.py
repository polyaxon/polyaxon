from rest_framework.generics import get_object_or_404

from api.endpoint.project import ProjectResourceEndpoint
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment


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
