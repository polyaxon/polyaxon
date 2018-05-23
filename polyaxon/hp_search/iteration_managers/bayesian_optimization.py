from hp_search.iteration_managers.base import BaseIterationManger
from hp_search.schemas.bayesian_optimization import BOIterationConfig


class BOIterationManager(BaseIterationManger):
    def get_metric_name(self):
        return self.experiment_group.params_config.bo.metric.name

    def create_iteration(self, experiment_ids, experiments_configs):
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
            old_experiment_ids=old_experiment_ids,
            old_experiments_configs=old_experiments_configs,
            old_experiments_metrics=old_experiments_metrics,
            experiment_ids=experiment_ids,
            experiments_configs=experiments_configs,
        )
        return ExperimentGroupIteration.objects.create(
            experiment_group=self.experiment_group,
            data=iteration_config.to_dict())
