from constants.statuses import BaseStatuses


class ExperimentGroupLifeCycle(BaseStatuses):
    """Experiment group lifecycle

    Props:
        * CREATED: created and waiting to be scheduled
        * RUNNING: one or all jobs is still running
        * SUCCEEDED: master and workers have finished successfully
        * FAILED: one of the jobs has failed
        * STOPPED: was stopped/deleted/killed
    """
    CREATED = 'created'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    STOPPED = 'stopped'

    CHOICES = (
        (CREATED, CREATED),
        (RUNNING, RUNNING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
        (STOPPED, STOPPED),
    )

    VALUES = {
        CREATED, RUNNING, SUCCEEDED, FAILED, STOPPED
    }

    PENDING_STATUS = {CREATED, }
    RUNNING_STATUS = {RUNNING, }
    DONE_STATUS = {FAILED, STOPPED, SUCCEEDED}
    FAILED_STATUS = {FAILED, }

    TRANSITION_MATRIX = {
        CREATED: {None, },
        RUNNING: {CREATED, STOPPED},
        SUCCEEDED: {RUNNING, },
        FAILED: {CREATED, RUNNING},
        STOPPED: set(VALUES),
    }
