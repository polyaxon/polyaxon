from hpsearch.iteration_managers.base import BaseIterationManager
from hpsearch.schemas.bayesian_optimization import BOIterationConfig


class BOIterationManager(BaseIterationManager):
    def get_metric_name(self):
        return self.experiment_group.hptuning_config.bo.metric.name

    def create_iteration(self, num_suggestions):
        """Create an iteration for the experiment group."""
        from db.models.experiment_groups import ExperimentGroupIteration

        iteration_config = self.experiment_group.iteration_config

        if iteration_config is None:
            iteration = 0
            old_experiment_ids = None
            old_experiments_configs = None
            old_experiments_metrics = None
        else:
            iteration = iteration_config.iteration + 1
            old_experiment_ids = iteration_config.combined_experiment_ids
            old_experiments_configs = iteration_config.combined_experiments_configs
            old_experiments_metrics = iteration_config.combined_experiments_metrics

        # Create a new iteration config
        iteration_config = BOIterationConfig(
            iteration=iteration,
            num_suggestions=num_suggestions,
            old_experiment_ids=old_experiment_ids,
            old_experiments_configs=old_experiments_configs,
            old_experiments_metrics=old_experiments_metrics,
            experiment_ids=[],
            experiments_configs=[],
        )
        return ExperimentGroupIteration.objects.create(
            experiment_group=self.experiment_group,
            data=iteration_config.to_dict())

    def update_iteration(self):
        """Update the last experiment group's iteration with experiment performance."""
        iteration_config = self.get_iteration_config()
        if not iteration_config:
            return
        experiments_metrics = self.experiment_group.get_experiments_metrics(
            experiment_ids=iteration_config.experiment_ids,
            metric=self.get_metric_name()
        )
        experiments_configs = self.experiment_group.get_experiments_declarations(
            experiment_ids=iteration_config.experiment_ids
        )
        iteration_config.experiments_configs = list(experiments_configs)
        iteration_config.experiments_metrics = [m for m in experiments_metrics if m[1] is not None]
        self._update_config(iteration_config)
