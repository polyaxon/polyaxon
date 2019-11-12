from polyaxon.automl.schemas.iteration import BaseIterationConfig
from polyaxon.logger import logger


class BaseIterationManager(object):
    def __init__(self, experiment_group):
        self.experiment_group = experiment_group

    def create_iteration(self, num_suggestions):
        """Create an iteration for the experiment group (works for grid and random)."""
        from db.models.experiment_groups import ExperimentGroupIteration

        iteration_config = BaseIterationConfig(
            iteration=0, num_suggestions=num_suggestions, experiment_ids=[]
        )

        return ExperimentGroupIteration.objects.create(
            experiment_group=self.experiment_group, data=iteration_config.to_dict()
        )

    def get_metric_name(self):
        return None

    def get_iteration_config(self):
        iteration_config = self.experiment_group.iteration_config
        if iteration_config is None:
            logger.warning(
                "Experiment group `%s` attempted to update iteration, but has no iteration",
                self.experiment_group.id,
            )
            return None
        return iteration_config

    def _update_config(self, iteration_config):
        iteration = self.experiment_group.iteration
        iteration.data = iteration_config.to_dict()
        iteration.save()

    def update_iteration(self):
        """Update the last experiment group's iteration with experiment performance."""
        iteration_config = self.get_iteration_config()
        if not iteration_config:
            return
        experiments_metrics = self.experiment_group.get_experiments_metrics(
            experiment_ids=iteration_config.experiment_ids,
            metric=self.get_metric_name(),
        )
        iteration_config.experiments_metrics = [
            m for m in experiments_metrics if m[1] is not None
        ]
        self._update_config(iteration_config)

    def update_iteration_num_suggestions(self, num_suggestions):
        """Update iteration's num_suggestions."""
        iteration_config = self.experiment_group.iteration_config

        iteration_config.num_suggestions = num_suggestions
        self._update_config(iteration_config)

    def add_iteration_experiments(self, experiment_ids):
        iteration = self.experiment_group.iteration
        if not iteration:
            logger.warning(
                "Experiment group `%s` attempted to update iteration, but has no iteration",
                self.experiment_group.id,
            )
            return

        iteration.experiments.add(*experiment_ids)
