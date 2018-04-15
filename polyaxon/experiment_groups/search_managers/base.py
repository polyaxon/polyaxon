class BaseSearchAlgorithmManager(object):
    NAME = None

    def __init__(self, params_config):
        self.params_config = params_config

    def get_suggestions(self, iteration=None):
        raise NotImplemented  # noqa
