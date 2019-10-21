import copy


def get_labels(default_labels, labels=None):
    labels = labels or {}
    _labels = copy.copy(labels)
    _labels.update(default_labels)
    return _labels
