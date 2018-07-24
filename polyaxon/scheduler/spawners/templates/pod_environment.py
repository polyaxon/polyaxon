import json


def _get_valid_dict_or_default(value, default_value):
    if value:
        return value
    value = default_value
    return json.loads(value) if value else None


def get_affinity(affinity, default_affinity):
    return _get_valid_dict_or_default(affinity, default_affinity)


def get_tolerations(tolerations, default_tolerations):
    return _get_valid_dict_or_default(tolerations, default_tolerations)


def get_node_selector(node_selector, default_node_selector):
    return _get_valid_dict_or_default(node_selector, default_node_selector)
