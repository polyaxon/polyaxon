from hestia.unknown import UNKNOWN

from lifecycles.statuses import BaseStatuses, StatusOptions


class PipelineLifeCycle(BaseStatuses):
    CREATED = StatusOptions.CREATED
    WARNING = StatusOptions.WARNING
    SCHEDULED = StatusOptions.SCHEDULED
    RUNNING = StatusOptions.RUNNING
    DONE = StatusOptions.DONE
    STOPPED = StatusOptions.STOPPED
    STOPPING = StatusOptions.STOPPING
    SKIPPED = StatusOptions.SKIPPED
    FAILED = StatusOptions.FAILED
    UPSTREAM_FAILED = StatusOptions.UPSTREAM_FAILED
    SUCCEEDED = StatusOptions.SUCCEEDED
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (WARNING, WARNING),
        (SCHEDULED, SCHEDULED),
        (RUNNING, RUNNING),
        (DONE, DONE),
        (FAILED, FAILED),
        (UPSTREAM_FAILED, UPSTREAM_FAILED),
        (STOPPED, STOPPED),
        (SUCCEEDED, SUCCEEDED),
        (STOPPING, STOPPING),
        (SKIPPED, SKIPPED),
        (UNKNOWN, UNKNOWN),
    )

    VALUES = {
        CREATED,
        WARNING,
        SCHEDULED,
        RUNNING,
        DONE,
        FAILED,
        UPSTREAM_FAILED,
        STOPPED,
        SUCCEEDED,
        STOPPING,
        SKIPPED,
        UNKNOWN
    }

    HEARTBEAT_STATUS = set([])
    WARNING_STATUS = {WARNING, }
    STARTING_STATUS = {CREATED, }
    RUNNING_STATUS = {SCHEDULED, RUNNING, STOPPING, }
    DONE_STATUS = {FAILED, UPSTREAM_FAILED, DONE, STOPPED, SKIPPED, SUCCEEDED, }
    FAILED_STATUS = {FAILED, UPSTREAM_FAILED, }

    TRANSITION_MATRIX = {
        CREATED: {None, },
        SCHEDULED: {CREATED, WARNING, },
        RUNNING: {CREATED, SCHEDULED, WARNING, },
        WARNING: set(VALUES) - {DONE, STOPPED, SKIPPED, STOPPED, WARNING, },
        DONE: set(VALUES) - DONE_STATUS,
        FAILED: set(VALUES) - DONE_STATUS,
        UPSTREAM_FAILED: set(VALUES) - DONE_STATUS,
        SUCCEEDED: set(VALUES) - DONE_STATUS,
        STOPPED: set(VALUES) - DONE_STATUS,
        STOPPING: VALUES - DONE_STATUS - {STOPPING, },
        SKIPPED: set(VALUES) - DONE_STATUS,
        UNKNOWN: VALUES - {UNKNOWN, },
    }


class TriggerPolicy(object):
    ALL_SUCCEEDED = 'all_succeeded'
    ALL_FAILED = 'all_failed'
    ALL_DONE = 'all_done'
    ONE_SUCCEEDED = 'one_succeeded'
    ONE_FAILED = 'one_failed'
    ONE_DONE = 'one_done'

    VALUES = {ALL_SUCCEEDED, ALL_FAILED, ALL_DONE, ONE_SUCCEEDED, ONE_FAILED, ONE_DONE}
    CHOICES = (
        (ALL_SUCCEEDED, ALL_SUCCEEDED),
        (ALL_FAILED, ALL_FAILED),
        (ALL_DONE, ALL_DONE),
        (ONE_SUCCEEDED, ONE_SUCCEEDED),
        (ONE_FAILED, ONE_FAILED),
        (ONE_DONE, ONE_DONE),
    )
