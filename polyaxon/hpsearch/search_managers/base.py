class BaseSearchAlgorithmManager(object):
    NAME = None

    def __init__(self, hptuning_config):
        self.hptuning_config = hptuning_config
        if self.NAME != self.hptuning_config.search_algorithm:
            raise ValueError(
                'The current search manger `{}` is not compatible '
                'with the search algorithm `{}` defined in the config.'.format(
                    self.NAME, self.hptuning_config.search_algorithm))

    def get_suggestions(self, iteration_config=None):
        raise NotImplementedError  # noqa

    def get_num_suggestions(self, iteration_config):
        return iteration_config.num_suggestions

    def scheduled_all_suggestions(self, iteration_config):
        raise iteration_config.num_suggestions == len(iteration_config.experiment_ids)
