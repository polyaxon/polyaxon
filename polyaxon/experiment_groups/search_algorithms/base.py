class BaseSearchAlgorithm(object):
    NAME = None

    def __init__(self, specification):
        self.specification = specification

    def get_suggestions(self):
        raise NotImplemented
