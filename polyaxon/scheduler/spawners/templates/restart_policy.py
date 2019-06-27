def get_max_restart(max_restarts, default):
    return max_restarts or default


def get_restart_policy(max_restarts):
    if not max_restarts:
        return 'Never'
    return 'OnFailure'
