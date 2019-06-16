def get_affinity(affinity, default_affinity):
    return affinity or default_affinity


def get_tolerations(tolerations, default_tolerations):
    return tolerations or default_tolerations


def get_node_selector(node_selector, default_node_selector):
    return node_selector or default_node_selector


def get_pod_resources(resources, default_resources):
    return resources or default_resources
