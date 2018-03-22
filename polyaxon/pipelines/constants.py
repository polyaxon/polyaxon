class CeleryTaskStatus(object):
    PENDING = 'PENDING'
    STARTED = 'STARTED'
    RETRY = 'RETRY'
    FAILURE = 'FAILURE'
    SUCCESS = 'SUCCESS'


class TaskStatus(object):
    STARTED = 'started'
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    SKIPPED = 'skipped'
    RETRYING = 'retrying'

    VALUES = [STARTED, PENDING, RUNNING, SUCCESS, FAILED, SKIPPED, RETRYING]
    CHOICES = (
        (STARTED, STARTED),
        (RUNNING, RUNNING),
        (SUCCESS, SUCCESS),
        (FAILED, FAILED),
        (SKIPPED, SKIPPED),
        (RETRYING, RETRYING)
    )

    DONE_STATUS = [SUCCESS, FAILED]


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
