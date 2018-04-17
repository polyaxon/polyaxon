class BaseSearchAlgorithmManager(object):
    NAME = None

    def __init__(self, params_config):
        self.params_config = params_config
        if self.NAME != self.params_config.search_algorithm:
            raise ValueError(
                'The current search manger `{}` is not compatible '
                'with the search algorithm `{}` defined in the config.'.format(
                    self.NAME, self.params_config.search_algorithm))

    def get_suggestions(self, iteration=None):
        raise NotImplemented  # noqa
