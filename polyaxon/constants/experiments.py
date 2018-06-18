from constants.jobs import JobLifeCycle
from constants.statuses import BaseStatuses
from constants.unknown import UNKNOWN


class ExperimentLifeCycle(BaseStatuses):
    """Experiment lifecycle

    Props:
        * CREATED: created and waiting to be scheduled
        * BUILDING: started building imagesif necessary
        * SCHEDULED: scheduled waiting to be picked
        * STARTING: picked and is starting (jobs are created/building/pending)
        * RUNNING: one or all jobs is still running
        * SUCCEEDED: master and workers have finished successfully
        * FAILED: one of the jobs has failed
        * STOPPED: was stopped/deleted/killed
        * UNKNOWN: unknown state
    """
    CREATED = 'created'
    RESUMING = 'resuming'
    BUILDING = 'building'
    SCHEDULED = 'scheduled'
    STARTING = 'starting'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    STOPPED = 'stopped'
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (RESUMING, RESUMING),
        (BUILDING, BUILDING),
        (SCHEDULED, SCHEDULED),
        (STARTING, STARTING),
        (RUNNING, RUNNING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
        (STOPPED, STOPPED),
        (UNKNOWN, UNKNOWN),
    )

    VALUES = {
        CREATED, RESUMING, BUILDING, SCHEDULED, STARTING, RUNNING,
        SUCCEEDED, FAILED, STOPPED, UNKNOWN
    }

    PENDING_STATUS = {CREATED, RESUMING}
    RUNNING_STATUS = {SCHEDULED, BUILDING, STARTING, RUNNING}
    DONE_STATUS = {FAILED, STOPPED, SUCCEEDED}
    FAILED_STATUS = {FAILED, }

    TRANSITION_MATRIX = {
        CREATED: {None, },
        RESUMING: {SUCCEEDED, STOPPED, },
        BUILDING: {CREATED, RESUMING, },
        SCHEDULED: {CREATED, RESUMING, BUILDING, },
        STARTING: {SCHEDULED, },
        RUNNING: {SCHEDULED, STARTING, UNKNOWN},
        SUCCEEDED: {SCHEDULED, STARTING, RUNNING, UNKNOWN, },
        FAILED: {CREATED, RESUMING, BUILDING, SCHEDULED, STARTING, RUNNING, UNKNOWN, },
        STOPPED: set(VALUES),
    }

    @staticmethod
    def jobs_starting(job_statuses):
        return any([True if JobLifeCycle.is_starting(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_running(job_statuses):
        return any([True if JobLifeCycle.is_running(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_succeeded(job_statuses):
        return all([True if job_status == JobLifeCycle.SUCCEEDED else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_failed(job_statuses):
        return any([True if job_status == JobLifeCycle.FAILED else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_stopped(job_statuses):
        return any([True if job_status == JobLifeCycle.STOPPED else False
                    for job_status in job_statuses])

    @classmethod
    def jobs_unknown(cls, job_statuses):
        return any([True if job_status == JobLifeCycle.UNKNOWN else False
                    for job_status in job_statuses])

    @classmethod
    def jobs_status(cls, job_statuses):
        if not job_statuses:
            return None

        if cls.jobs_unknown(job_statuses):
            return cls.UNKNOWN

        if cls.jobs_stopped(job_statuses):
            return cls.STOPPED

        if cls.jobs_succeeded(job_statuses):
            return cls.SUCCEEDED

        if cls.jobs_failed(job_statuses):
            return cls.FAILED

        if cls.jobs_starting(job_statuses):
            return cls.STARTING

        if cls.jobs_running(job_statuses):
            return cls.RUNNING

        return cls.UNKNOWN
