import copy
import logging

from experiment_groups.iteration_managers.base import BaseIterationManger
from experiment_groups.schemas.bayesian_optimization import BOIterationConfig

logger = logging.getLogger('polyaxon.experiments_groups.iteration_manager')


class BOIterationManager(BaseIterationManger):
    @staticmethod
    def get_combined_experiment_ids(iteration_config):
        experiment_ids = iteration_config.experiment_ids or []
        experiment_ids += iteration_config.new_experiment_ids or []
        return experiment_ids

    @staticmethod
    def get_combined_experiments_configs(iteration_config):
        experiments_configs = copy.deepcopy(iteration_config.experiments_configs) or {}
        experiments_configs.update(iteration_config.new_experiments_configs or {})
        return experiments_configs

    @staticmethod
    def get_combined_experiments_metrics(iteration_config):
        experiments_metrics = copy.deepcopy(iteration_config.experiments_metrics) or {}
        experiments_metrics.update(iteration_config.new_experiments_metrics or {})
        return experiments_metrics

    def create_iteration(self, new_experiment_ids, new_experiments_configs):
        """Create an iteration for the experiment group."""
        from experiment_groups.models import ExperimentGroupIteration

        iteration_config = self.experiment_group.iteration_config

        if iteration_config is None:
            iteration = 0
            experiment_ids = None
            experiments_configs = None
            experiments_metrics = None
        else:
            iteration = iteration_config.iteration + 1
            experiment_ids = self.get_combined_experiment_ids(iteration_config)
            experiments_configs = self.get_combined_experiments_configs(iteration_config)
            experiments_metrics = self.get_combined_experiments_metrics(iteration_config)

        # Create a new iteration config
        iteration_config = BOIterationConfig(
            iteration=iteration,
            experiment_ids=experiment_ids,
            experiments_configs=experiments_configs,
            experiments_metrics=experiments_metrics,
            new_experiment_ids=new_experiment_ids,
            new_experiments_configs=new_experiments_configs,
        )
        return ExperimentGroupIteration.objects.create(
            experiment_group=self.experiment_group,
            data=iteration_config.to_dict())
