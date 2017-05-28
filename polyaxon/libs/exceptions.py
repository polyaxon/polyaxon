class EstimatorNotTrainedError(Exception):
    """Exception class to raise if estimator is used before being trained."""
    pass


class ModuleNotBuiltError(Exception):
    """Exception class to raise if graph module is used before being built."""
    pass
