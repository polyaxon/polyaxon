from libs.constants import UNKNOWN


def to_bytes(size_str):
    try:
        return int(float(size_str))
    except (ValueError, TypeError):
        pass

    fixed_point_unit_multiplier = {
        'k': 1000,
        'm': 1000 ** 2,
        'g': 1000 ** 3,
        't': 1000 ** 4
    }

    power_two_unit_multiplier = {
        'ki': 1024,
        'mi': 1024 ** 2,
        'gi': 1024 ** 3,
        'ti': 1024 ** 4
    }

    if size_str[-2:].lower() in power_two_unit_multiplier.keys():
        return int(size_str[:-2]) * power_two_unit_multiplier.get(size_str[-2:].lower(), 1)

    if size_str[-1].lower() in fixed_point_unit_multiplier.keys():
        return int(size_str[:-1]) * fixed_point_unit_multiplier.get(size_str[-1].lower(), 1)

    return 0


class EventTypes(object):
    ADDED = 'ADDED'
    MODIFIED = 'MODIFIED'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


class ContainerStatuses(object):
    RUNNING = 'running'
    WAITING = 'waiting'
    TERMINATED = 'terminated'


class PodConditions(object):
    READY = 'Ready'
    INITIALIZED = 'Initialized'
    SCHEDULED = 'PodScheduled'

    VALUES = [READY, INITIALIZED, SCHEDULED]


class PodLifeCycle(object):
    CONTAINER_CREATING = 'ContainerCreating'
    PENDING = 'Pending'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    UNKNOWN = UNKNOWN

    CHOICES = (
        (RUNNING, RUNNING),
        (PENDING, PENDING),
        (CONTAINER_CREATING, CONTAINER_CREATING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
    )

    DONE_STATUS = [FAILED, SUCCEEDED]
