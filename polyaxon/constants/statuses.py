from hestia.unknown import UNKNOWN


class StatusOptions:
    CREATED = 'created'
    SCHEDULED = 'scheduled'
    UNSCHEDULABLE = 'unschedulable'
    WARNING = 'warning'
    BUILDING = 'building'
    RESUMING = 'resuming'
    STARTING = 'starting'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    UPSTREAM_FAILED = 'upstream_failed'
    STOPPING = 'stopping'
    STOPPED = 'stopped'
    FINISHED = 'finished'
    SKIPPED = 'skipped'
    RETRYING = 'retrying'
    DONE = 'done'


class BaseStatuses(object):
    VALUES = set([])
    CHOICES = ()
    HEARTBEAT_STATUS = set([])
    WARNING_STATUS = set([])
    STARTING_STATUS = set([])
    DONE_STATUS = set([])
    RUNNING_STATUS = set([])
    FAILED_STATUS = set([])
    # Defines the transition matrix: {desired_status: set(possible_statuses)}
    TRANSITION_MATRIX = {}

    @classmethod
    def can_transition(cls, status_from: str, status_to: str) -> bool:
        if status_to not in cls.TRANSITION_MATRIX:
            return False

        return status_from in cls.TRANSITION_MATRIX[status_to]

    @classmethod
    def is_unschedulable(cls, status: str) -> bool:
        return status == StatusOptions.UNSCHEDULABLE

    @classmethod
    def is_warning(cls, status: str) -> bool:
        return status in cls.WARNING_STATUS

    @classmethod
    def is_starting(cls, status: str) -> bool:
        return status in cls.STARTING_STATUS

    @classmethod
    def is_running(cls, status: str) -> bool:
        return status in cls.RUNNING_STATUS

    @classmethod
    def is_unknown(cls, status: str) -> bool:
        return status == UNKNOWN

    @classmethod
    def is_stoppable(cls, status: str) -> bool:
        return (cls.is_running(status=status) or
                cls.is_unschedulable(status=status) or
                cls.is_warning(status=status) or
                cls.is_unknown(status=status))

    @classmethod
    def is_done(cls, status: str) -> bool:
        return status in cls.DONE_STATUS

    @classmethod
    def failed(cls, status: str) -> bool:
        return status in cls.FAILED_STATUS

    @classmethod
    def done(cls, status: str) -> bool:
        return status == cls.DONE

    @classmethod
    def succeeded(cls, status: str) -> bool:
        return status == cls.SUCCEEDED

    @classmethod
    def stopped(cls, status: str) -> bool:
        return status == cls.STOPPED

    @classmethod
    def skipped(cls, status: str) -> bool:
        return status == cls.SKIPPED
