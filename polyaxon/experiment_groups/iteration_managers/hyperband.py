import logging

from experiment_groups.iteration_managers.base import BaseIterationManger
from experiment_groups.schemas import HyperbandIterationConfig
from polyaxon_schemas.utils import Optimization

logger = logging.getLogger('polyaxon.experiments_groups.iteration_manager')


class HyperbandIterationManager(BaseIterationManger):
    def create_iteration(self, experiment_ids):
        """Create an iteration for the experiment group."""
        from experiment_groups.models import ExperimentGroupIteration

        iteration_config = self.experiment_group.iteration_config

        # Create a new iteration config
        iteration_config = HyperbandIterationConfig(
            iteration=1 if iteration_config is None else iteration_config.iteration,
            bracket_iteration=0,
            experiment_ids=experiment_ids)
        return ExperimentGroupIteration.objects.create(
            experiment_group=self.experiment_group,
            data=iteration_config.to_dict())

    def update_iteration(self):
        """Update the last experiment group's iteration with experiment performance."""
        iteration_config = self.experiment_group.iteration_config
        if iteration_config is None:
            logger.warning(
                'Experiment group `%s` attempt to update, but has no iteration',
                self.experiment_group.id)
            return
        experiments_metrics = self.experiment_group.get_experiments_metrics(
            experiment_ids=iteration_config.experiment_ids,
            metric=self.experiment_group.params_config.hyperband.metric.name,
        )
        iteration_config.experiments_metrics = [m for m in experiments_metrics if m[1] is not None]
        iteration = self.experiment_group.iteration
        iteration.data = iteration_config.to_dict()
        iteration.save()

    def get_reduced_configs(self):
        """Reduce the experiments to restart."""
        iteration_config = self.experiment_group.iteration_config
        if iteration_config is None:
            logger.warning(
                'Experiment group `%s` attempt to update, but has no iteration',
                self.experiment_group.id)
            return
        search_manager = self.experiment_group.search_manager

        # Get the number of experiments to keep
        n_configs_to_keep = search_manager.get_n_config_to_keep_for_iteration(
            iteration=iteration_config.iteration,
            bracket_iteration=iteration_config.bracket_iteration)

        # Get the last group's experiments metrics
        experiments_metrics = self.experiment_group.iteration_config.experiments_metrics

        # Order the experiments
        reverse = Optimization.maximize(
            self.experiment_group.params_config.hyperband.metric.optimization)
        experiments_metrics = sorted(experiments_metrics, key=lambda x: x[1], reverse=reverse)

        # Keep n experiments
        return [xp[0] for xp in experiments_metrics[:n_configs_to_keep]]

    def reduce_configs(self):
        """Reduce the experiments to restart."""
        experiment_ids = self.get_reduced_configs()
        experiments = self.experiment_group.experiments.filter(id__in=experiment_ids)
        iteration_config = self.experiment_group.iteration_config
        status_message = 'Hyperband iteration: {}, bracket iteration: {}'.format(
            iteration_config.iteration,
            iteration_config.bracket_iteration
        )
        resource_value = self.experiment_group.search_manager.get_resources_for_iteration(
            iteration=iteration_config.iteration)
        resource_name = self.experiment_group.params_config.hyperband.resource

        # Check if we need to resume or restart the experiments
        if self.experiment_group.params_config.hyperband.resume:
            for experiment in experiments:
                declarations = experiment.declarations
                declarations[resource_name] = resource_value
                experiment.resume(declarations=declarations, message=status_message)
        else:
            for experiment in experiments:
                declarations = experiment.declarations
                declarations[resource_name] = resource_value
                experiment.restart(
                    experiment_group=self.experiment_group,
                    declarations=declarations)
