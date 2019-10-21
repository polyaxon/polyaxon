from hestia.unknown import UNKNOWN

from lifecycles.statuses import BaseStatuses, StatusOptions


class ExperimentGroupLifeCycle(BaseStatuses):
    CREATED = StatusOptions.CREATED
    RESUMING = StatusOptions.RESUMING
    RUNNING = StatusOptions.RUNNING
    WARNING = StatusOptions.WARNING
    DONE = StatusOptions.DONE
    FAILED = StatusOptions.FAILED
    UPSTREAM_FAILED = StatusOptions.UPSTREAM_FAILED
    STOPPING = StatusOptions.STOPPING
    STOPPED = StatusOptions.STOPPED
    SKIPPED = StatusOptions.SKIPPED
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (RESUMING, RESUMING),
        (RUNNING, RUNNING),
        (WARNING, WARNING),
        (DONE, DONE),
        (FAILED, FAILED),
        (UPSTREAM_FAILED, UPSTREAM_FAILED),
        (STOPPING, STOPPING),
        (STOPPED, STOPPED),
        (SKIPPED, SKIPPED),
        (UNKNOWN, UNKNOWN),
    )

    VALUES = {
        CREATED,
        RESUMING,
        RUNNING,
        WARNING,
        DONE,
        FAILED,
        UPSTREAM_FAILED,
        STOPPING,
        STOPPED,
        SKIPPED,
        UNKNOWN
    }

    WARNING_STATUS = {WARNING, }
    PENDING_STATUS = {CREATED, RESUMING, }
    RUNNING_STATUS = {RUNNING, STOPPING, }
    DONE_STATUS = {FAILED, UPSTREAM_FAILED, STOPPED, SKIPPED, DONE, }
    FAILED_STATUS = {FAILED, UPSTREAM_FAILED, }

    TRANSITION_MATRIX = {
        CREATED: {None, },
        RESUMING: {CREATED, WARNING, SKIPPED, STOPPED, },
        RUNNING: {CREATED, RESUMING, WARNING, },
        DONE: VALUES - DONE_STATUS,
        SKIPPED: VALUES - DONE_STATUS,
        FAILED: VALUES - DONE_STATUS,
        UPSTREAM_FAILED: VALUES - DONE_STATUS,
        STOPPING: VALUES - DONE_STATUS - {STOPPING, },
        STOPPED: VALUES - DONE_STATUS,
        WARNING: VALUES - DONE_STATUS - {WARNING, },
        UNKNOWN: VALUES - {UNKNOWN, },
    }
