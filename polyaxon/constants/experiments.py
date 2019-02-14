from typing import List, Optional

from hestia.unknown import UNKNOWN

from constants.jobs import JobLifeCycle
from constants.statuses import BaseStatuses, StatusOptions


class ExperimentLifeCycle(BaseStatuses):
    """Experiment lifecycle

    Props:
        * CREATED: created and waiting to be scheduled
        * BUILDING: started building images if necessary
        * SCHEDULED: scheduled waiting to be picked
        * STARTING: picked and is starting (jobs are created/building/pending)
        * RUNNING: one or all jobs is still running
        * SUCCEEDED: master and workers have finished successfully
        * FAILED: one of the jobs has failed
        * STOPPED: was stopped/deleted/killed
        * UNKNOWN: unknown state
    """
    CREATED = StatusOptions.CREATED
    RESUMING = StatusOptions.RESUMING
    WARNING = StatusOptions.WARNING
    UNSCHEDULABLE = StatusOptions.UNSCHEDULABLE
    BUILDING = StatusOptions.BUILDING
    SCHEDULED = StatusOptions.SCHEDULED
    STARTING = StatusOptions.STARTING
    RUNNING = StatusOptions.RUNNING
    SUCCEEDED = StatusOptions.SUCCEEDED
    FAILED = StatusOptions.FAILED
    STOPPED = StatusOptions.STOPPED
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (RESUMING, RESUMING),
        (WARNING, WARNING),
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
        CREATED, RESUMING, WARNING, BUILDING, SCHEDULED, STARTING, RUNNING,
        SUCCEEDED, FAILED, STOPPED, UNKNOWN
    }

    HEARTBEAT_STATUS = {RUNNING, }
    WARNING_STATUS = {WARNING, }
    PENDING_STATUS = {CREATED, RESUMING}
    RUNNING_STATUS = {SCHEDULED, BUILDING, STARTING, RUNNING}
    DONE_STATUS = {FAILED, STOPPED, SUCCEEDED}
    FAILED_STATUS = {FAILED, }

    TRANSITION_MATRIX = {
        CREATED: {None, },
        RESUMING: {CREATED, WARNING, SUCCEEDED, STOPPED, },
        BUILDING: {CREATED, RESUMING, WARNING, UNKNOWN, },
        SCHEDULED: {CREATED, RESUMING, BUILDING, WARNING, UNKNOWN, },
        STARTING: {CREATED, RESUMING, BUILDING, SCHEDULED, WARNING, },
        RUNNING: {CREATED, RESUMING, BUILDING, SCHEDULED, STARTING, WARNING, UNKNOWN},
        SUCCEEDED: {CREATED, RESUMING, BUILDING, SCHEDULED, STARTING, RUNNING, WARNING, UNKNOWN, },
        FAILED: {CREATED, RESUMING, BUILDING, SCHEDULED, STARTING, RUNNING, WARNING, UNKNOWN, },
        STOPPED: set(VALUES) - {STOPPED, },
        WARNING: set(VALUES) - {SUCCEEDED, FAILED, STOPPED, WARNING, },
        UNKNOWN: set(VALUES) - {UNKNOWN, },
    }

    @staticmethod
    def jobs_unschedulable(job_statuses: List[str]) -> bool:
        return any([True if JobLifeCycle.is_unschedulable(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_warning(job_statuses: List[str]) -> bool:
        return any([True if JobLifeCycle.is_warning(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_starting(job_statuses: List[str]) -> bool:
        return any([True if JobLifeCycle.is_starting(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_running(job_statuses: List[str]) -> bool:
        return any([True if JobLifeCycle.is_running(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_succeeded(job_statuses: List[str]) -> bool:
        return all([True if job_status == JobLifeCycle.SUCCEEDED else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_failed(job_statuses: List[str]) -> bool:
        return any([True if job_status == JobLifeCycle.FAILED else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_stopped(job_statuses: List[str]) -> bool:
        return any([True if job_status == JobLifeCycle.STOPPED else False
                    for job_status in job_statuses])

    @classmethod
    def jobs_unknown(cls, job_statuses: List[str]) -> bool:
        return any([True if job_status == JobLifeCycle.UNKNOWN else False
                    for job_status in job_statuses])

    @classmethod
    def jobs_status(cls, job_statuses: List[str]) -> Optional[str]:
        if not job_statuses:
            return None

        if cls.jobs_unknown(job_statuses):
            return cls.UNKNOWN

        if cls.jobs_unschedulable(job_statuses):
            return cls.UNSCHEDULABLE

        if cls.jobs_warning(job_statuses):
            return cls.WARNING

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
