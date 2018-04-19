import logging

from experiment_groups.iteration_managers.base import BaseIterationManger
from experiment_groups.schemas import HyperbandIterationConfig
from polyaxon_schemas.polyaxonfile.specification import ExperimentSpecification
from polyaxon_schemas.utils import Optimization

logger = logging.getLogger('polyaxon.experiments_groups.iteration_manager')


class HyperbandIterationManager(BaseIterationManger):
    def create_iteration(self, experiment_ids=None):
        """Create an iteration for the experiment group."""
        from experiment_groups.models import ExperimentGroupIteration

        search_manager = self.experiment_group.search_manager
        iteration_config = self.experiment_group.iteration_config

        if iteration_config is None:
            iteration = 1
            bracket_iteration = 0
        else:
            should_reschedule = search_manager.should_reschedule(
                iteration=iteration_config.iteration,
                bracket_iteration=iteration_config.bracket_iteration)
            should_reduce_configs = search_manager.should_reduce_configs(
                iteration=iteration_config.iteration,
                bracket_iteration=iteration_config.bracket_iteration)
            if should_reschedule:
                iteration = iteration_config.iteration + 1
                bracket_iteration = 0
            elif should_reduce_configs:
                iteration = iteration_config.iteration
                bracket_iteration = iteration_config.bracket_iteration
            else:
                raise ValueError(
                    'Hyperband create iteration failed for `{}`, '
                    'could not reschedule ot reduce configs'.format(self.experiment_group.id))

        # Create a new iteration config
        iteration_config = HyperbandIterationConfig(
            iteration=iteration,
            bracket_iteration=bracket_iteration)
        if experiment_ids:
            iteration_config.experiment_ids = experiment_ids
        return ExperimentGroupIteration.objects.create(
            experiment_group=self.experiment_group,
            data=iteration_config.to_dict())

    def get_iteration_config(self):
        iteration_config = self.experiment_group.iteration_config
        if iteration_config is None:
            logger.warning(
                'Experiment group `%s` attempt to update, but has no iteration',
                self.experiment_group.id)
            return None
        return iteration_config

    def _update_config(self, iteration_config):
        iteration = self.experiment_group.iteration
        iteration.data = iteration_config.to_dict()
        iteration.save()

    def add_iteration_experiments(self, experiment_ids):
        iteration_config = self.get_iteration_config()
        if not iteration_config:
            return

        iteration_config.experiment_ids = experiment_ids
        self._update_config(iteration_config)

    def update_iteration(self):
        """Update the last experiment group's iteration with experiment performance."""
        iteration_config = self.get_iteration_config()
        if not iteration_config:
            return
        experiments_metrics = self.experiment_group.get_experiments_metrics(
            experiment_ids=iteration_config.experiment_ids,
            metric=self.experiment_group.params_config.hyperband.metric.name,
        )
        iteration_config.experiments_metrics = [m for m in experiments_metrics if m[1] is not None]
        self._update_config(iteration_config)

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
        self.create_iteration(experiment_ids=experiment_ids)
        iteration_config = self.experiment_group.iteration_config
        params_config = self.experiment_group.params_config
        resource_value = self.experiment_group.search_manager.get_resources_for_iteration(
            iteration=iteration_config.iteration)
        resource_name = params_config.hyperband.resource.name
        resource_value = params_config.hyperband.resource.cast_value(resource_value)

        # Check if we need to resume or restart the experiments
        for experiment in experiments:
            declarations = experiment.declarations
            declarations[resource_name] = resource_value
            declarations = {'declarations': declarations}
            specification = ExperimentSpecification(
                values=[experiment.specification.parsed_data, declarations])
            status_message = 'Hyperband iteration: {}, bracket iteration: {}'.format(
                iteration_config.iteration,
                iteration_config.bracket_iteration)

            if params_config.hyperband.resume:
                experiment.resume(
                    declarations=declarations,
                    config=specification.parsed_data,
                    message=status_message)
            else:
                experiment.restart(
                    experiment_group=self.experiment_group,
                    config=specification.parsed_data,
                    declarations=declarations)
