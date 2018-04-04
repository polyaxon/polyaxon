class ExperimentDeclaration(object):
    """A structure that defines an experiment declaration."""
    def __init__(self, params):
        self.params = params

    def __eq__(self, other):
        if self.params.keys() != other.keys():
            return False

        for key, value in self.params.items():
            if value != other.params[key]:
                return False

        return True
