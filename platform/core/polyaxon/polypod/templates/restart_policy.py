def get_max_restart(max_restarts, default):
    return max_restarts or default


def get_pod_restart_policy(max_restarts):
    if not max_restarts:
        return 'Never'
    return 'OnFailure'


def get_deployment_restart_policy(max_restarts):
    if not max_restarts:
        return None
    return 'Always'
