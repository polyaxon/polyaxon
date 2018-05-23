from libs.constants import UNKNOWN


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
