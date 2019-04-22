from typing import List, Optional

from hestia.unknown import UNKNOWN

from lifecycles.jobs import JobLifeCycle
from lifecycles.statuses import BaseStatuses, StatusOptions


class ExperimentLifeCycle(BaseStatuses):
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
    UPSTREAM_FAILED = StatusOptions.UPSTREAM_FAILED
    STOPPED = StatusOptions.STOPPED
    SKIPPED = StatusOptions.SKIPPED
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
        (UPSTREAM_FAILED, UPSTREAM_FAILED),
        (STOPPED, STOPPED),
        (SKIPPED, SKIPPED),
        (UNKNOWN, UNKNOWN),
    )

    VALUES = {
        CREATED,
        RESUMING,
        WARNING,
        BUILDING,
        SCHEDULED,
        STARTING,
        RUNNING,
        SUCCEEDED,
        FAILED,
        UPSTREAM_FAILED,
        STOPPED,
        SKIPPED,
        UNKNOWN
    }

    HEARTBEAT_STATUS = {RUNNING, }
    WARNING_STATUS = {WARNING, }
    PENDING_STATUS = {CREATED, RESUMING, }
    RUNNING_STATUS = {SCHEDULED, BUILDING, STARTING, RUNNING, }
    DONE_STATUS = {FAILED, UPSTREAM_FAILED, STOPPED, SKIPPED, SUCCEEDED, }
    FAILED_STATUS = {FAILED, UPSTREAM_FAILED, }

    TRANSITION_MATRIX = {
        CREATED: {None, },
        RESUMING: {CREATED, WARNING, SUCCEEDED, SKIPPED, STOPPED, },
        BUILDING: {CREATED, RESUMING, WARNING, UNKNOWN, },
        SCHEDULED: {CREATED, RESUMING, BUILDING, WARNING, UNKNOWN, },
        STARTING: {CREATED, RESUMING, BUILDING, SCHEDULED, WARNING, },
        RUNNING: {CREATED, RESUMING, BUILDING, SCHEDULED, STARTING, WARNING, UNKNOWN, },
        SKIPPED: VALUES - DONE_STATUS,
        SUCCEEDED: VALUES - DONE_STATUS,
        FAILED: VALUES - DONE_STATUS,
        UPSTREAM_FAILED: VALUES - DONE_STATUS,
        STOPPED: VALUES - {STOPPED, SKIPPED, },
        WARNING: VALUES - DONE_STATUS - {WARNING, },
        UNKNOWN: VALUES - DONE_STATUS - {UNKNOWN, },
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
