from libs.statuses import BaseStatuses


class PipelineStatuses(BaseStatuses):
    CREATED = 'created'
    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    FINISHED = 'finished'
    STOPPED = 'stopped'
    SKIPPED = 'skipped'

    VALUES = [
        CREATED, SCHEDULED, RUNNING, FINISHED, STOPPED, SKIPPED
    ]
    CHOICES = (
        (CREATED, CREATED),
        (SCHEDULED, SCHEDULED),
        (RUNNING, RUNNING),
        (FINISHED, FINISHED),
        (STOPPED, STOPPED),
        (SKIPPED, SKIPPED),
    )

    DONE_STATUS = [FINISHED, STOPPED, SKIPPED]
    RUNNING_STATUS = [SCHEDULED, RUNNING]
    FAILED_STATUS = []

    TRANSITION_MATRIX = {
        CREATED: set([]),
        SCHEDULED: {CREATED, },
        RUNNING: {SCHEDULED, },
        FINISHED: {SCHEDULED, RUNNING, },
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

    VALUES = [
        CREATED, SCHEDULED, RUNNING, SUCCEEDED, FAILED, UPSTREAM_FAILED, STOPPED, SKIPPED, RETRYING
    ]
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

    DONE_STATUS = [SUCCEEDED, FAILED, UPSTREAM_FAILED, STOPPED, SKIPPED]
    RUNNING_STATUS = [SCHEDULED, RUNNING]
    FAILED_STATUS = [FAILED, UPSTREAM_FAILED]

    TRANSITION_MATRIX = {
        CREATED: set([]),
        SCHEDULED: {CREATED, RETRYING, },
        RUNNING: {SCHEDULED, },
        SUCCEEDED: {RUNNING, },
        FAILED: {SCHEDULED, RUNNING, },
        UPSTREAM_FAILED: set(VALUES),
        STOPPED: {CREATED, SCHEDULED, RUNNING, },
        SKIPPED: {CREATED, SCHEDULED, STOPPED, },
        RETRYING: {SCHEDULED, FAILED, STOPPED, SKIPPED, RETRYING},
    }


class TriggerRule(object):
    ALL_SUCCESS = 'all_success'
    ALL_FAILED = 'all_failed'
    ALL_DONE = 'all_done'
    ONE_SUCCESS = 'one_success'
    ONE_FAILED = 'one_failed'
    ONE_DONE = 'one_done'

    VALUES = [ALL_SUCCESS, ALL_FAILED, ALL_DONE, ONE_SUCCESS, ONE_FAILED, ONE_DONE]
    CHOICES = (
        (ALL_SUCCESS, ALL_SUCCESS),
        (ALL_FAILED, ALL_FAILED),
        (ALL_DONE, ALL_DONE),
        (ONE_SUCCESS, ONE_SUCCESS),
        (ONE_FAILED, ONE_FAILED),
        (ONE_DONE, ONE_DONE),
    )
