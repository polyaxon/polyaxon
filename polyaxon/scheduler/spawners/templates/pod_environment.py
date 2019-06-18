from schemas import PodResourcesConfig


def get_affinity(affinity, default_affinity):
    return affinity or default_affinity


def get_tolerations(tolerations, default_tolerations):
    return tolerations or default_tolerations


def get_node_selector(node_selector, default_node_selector):
    return node_selector or default_node_selector


def get_pod_resources(resources, default_resources):
    if resources:
        return resources
    elif default_resources:
        if not isinstance(default_resources, PodResourcesConfig):
            return PodResourcesConfig.from_dict(default_resources)
        return default_resources
    return None


def get_secret_refs(secret_refs, default_secret_refs):
    # Validate secrets
    return secret_refs or default_secret_refs


def get_config_map_refs(config_map_refs, default_config_map_refs):
    # Validate config_maps
    return config_map_refs or default_config_map_refs


def get_env_vars(env_vars, default_env_vars):
    return get_env_vars or default_env_vars
