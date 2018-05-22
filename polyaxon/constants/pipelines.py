from libs.statuses import BaseStatuses


class PipelineStatuses(BaseStatuses):
    CREATED = 'created'
    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    FINISHED = 'finished'
    STOPPED = 'stopped'
    SKIPPED = 'skipped'

    VALUES = {
        CREATED, SCHEDULED, RUNNING, FINISHED, STOPPED, SKIPPED
    }
    CHOICES = (
        (CREATED, CREATED),
        (SCHEDULED, SCHEDULED),
        (RUNNING, RUNNING),
        (FINISHED, FINISHED),
        (STOPPED, STOPPED),
        (SKIPPED, SKIPPED),
    )

    DONE_STATUS = {FINISHED, STOPPED, SKIPPED}
    RUNNING_STATUS = {SCHEDULED, RUNNING}
    FAILED_STATUS = set([])

    TRANSITION_MATRIX = {
        CREATED: {None, },
        SCHEDULED: {CREATED, },
        RUNNING: {SCHEDULED, },
        FINISHED: {CREATED, SCHEDULED, RUNNING, },
        STOPPED: {CREATED, SCHEDULED, RUNNING, },
        SKIPPED: {CREATED, SCHEDULED, STOPPED, },
    }


class OperationStatuses(BaseStatuses):
    CREATED = 'created'
    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    UPSTREAM_FAILED = 'upstream_failed'
    STOPPED = 'stopped'
    SKIPPED = 'skipped'
    RETRYING = 'retrying'

    VALUES = {
        CREATED, SCHEDULED, RUNNING, SUCCEEDED, FAILED, UPSTREAM_FAILED, STOPPED, SKIPPED, RETRYING
    }
    CHOICES = (
        (CREATED, CREATED),
        (SCHEDULED, SCHEDULED),
        (RUNNING, RUNNING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
        (UPSTREAM_FAILED, UPSTREAM_FAILED),
        (STOPPED, STOPPED),
        (SKIPPED, SKIPPED),
        (RETRYING, RETRYING)
    )

    DONE_STATUS = {SUCCEEDED, FAILED, UPSTREAM_FAILED, STOPPED, SKIPPED}
    RUNNING_STATUS = {SCHEDULED, RUNNING}
    FAILED_STATUS = {FAILED, UPSTREAM_FAILED}

    TRANSITION_MATRIX = {
        CREATED: {None, },
        SCHEDULED: {CREATED, RETRYING, },
        RUNNING: {SCHEDULED, },
        SUCCEEDED: {RUNNING, },
        FAILED: {SCHEDULED, RUNNING, },
        UPSTREAM_FAILED: set(VALUES) - {UPSTREAM_FAILED, },
        STOPPED: {CREATED, SCHEDULED, RUNNING, },
        SKIPPED: {CREATED, SCHEDULED, STOPPED, },
        RETRYING: {SCHEDULED, RUNNING, FAILED, STOPPED, SKIPPED, RETRYING, },
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
