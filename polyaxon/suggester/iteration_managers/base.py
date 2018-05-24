import logging

_logger = logging.getLogger('polyaxon.suggester.iteration_manager')


class BaseIterationManger(object):
    def __init__(self, experiment_group):
        self.experiment_group = experiment_group

    def get_metric_name(self):
        return None

    def get_iteration_config(self):
        iteration_config = self.experiment_group.iteration_config
        if iteration_config is None:
            _logger.warning(
                'Experiment group `%s` attempt to update iteration, but has no iteration',
                self.experiment_group.id)
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
            metric=self.get_metric_name()
        )
        iteration_config.experiments_metrics = [m for m in experiments_metrics if m[1] is not None]
        self._update_config(iteration_config)

    def add_iteration_experiments(self, experiment_ids):
        iteration_config = self.get_iteration_config()
        if not iteration_config:
            return

        iteration_config.experiment_ids = experiment_ids
        self._update_config(iteration_config)
