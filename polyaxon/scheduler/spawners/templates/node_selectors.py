import json


def get_node_selector(node_selector, default_node_selector):
    if node_selector:
        return node_selector
    node_selector = default_node_selector
    return json.loads(node_selector) if node_selector else None
