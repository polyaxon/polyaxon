# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

UNKNOWN = 'UNKNOWN'


def to_bytes(size_str):
    unit_multiplier = {
        'Ki': 1024,
        'Mi': 1024 ** 2,
        'Gi': 1024 ** 3,
        'Ti': 1024 ** 4
    }

    return int(size_str[:-2]) * unit_multiplier.get(size_str[-2:], 1)


class NodeLifeCycle(object):
    UNKNOWN = UNKNOWN
    READY = 'Ready'
    NOT_READY = 'NotReady'
    DELETED = 'Deleted'

    CHOICES = (
        (UNKNOWN, UNKNOWN),
        (READY, READY),
        (NOT_READY, NOT_READY),
        (DELETED, DELETED)
    )


class NodeRoles(object):
    MASTER = 'master'
    AGENT = 'agent'

    CHOICES = (
        (MASTER, MASTER),
        (AGENT, AGENT)
    )


class EventTypes(object):
    ADDED = 'ADDED'
    MODIFIED = 'MODIFIED'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


class ContainerStatuses(object):
    RUNNING = 'running'
    WAITING = 'waiting'
    TERMINATED = 'terminated'


class PodConditions(object):
    READY = 'Ready'
    INITIALIZED = 'Initialized'
    SCHEDULED = 'PodScheduled'

    VALUES = [READY, INITIALIZED, SCHEDULED]


class PodLifeCycle(object):
    CONTAINER_CREATING = 'ContainerCreating'
    PENDING = 'Pending'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    UNKNOWN = UNKNOWN

    CHOICES = (
        (RUNNING, RUNNING),
        (PENDING, PENDING),
        (CONTAINER_CREATING, CONTAINER_CREATING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
    )

    DONE_STATUS = [FAILED, SUCCEEDED]


class JobLifeCycle(object):
    """Experiment lifecycle

    Props:
        * CREATED: created.
        * BUILDING: This includes time before being bound to a node,
                    as well as time spent pulling images onto the host.
        * RUNNING: The pod has been bound to a node and all of the containers have been started.
        * SUCCEEDED: All containers in the pod have voluntarily terminated with a
                     container exit code of 0, and the system is
                     not going to restart any of these containers.
        * FAILED: All containers in the pod have terminated,
                  and at least one container has terminated in a failure.
        * STOPPED: was stopped/deleted/killed
        * UNKNOWN: For some reason the state of the pod could not be obtained,
                   typically due to an error in communicating with the host of the pod.
    """
    CREATED = 'Created'
    BUILDING = 'Building'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    STOPPED = 'Stopped'
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (BUILDING, BUILDING),
        (RUNNING, RUNNING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
        (STOPPED, STOPPED),
        (UNKNOWN, UNKNOWN),
    )

    STARTING_STATUS = [CREATED, BUILDING]
    RUNNING_STATUS = [BUILDING, RUNNING]
    DONE_STATUS = [FAILED, STOPPED, SUCCEEDED]

    @classmethod
    def is_starting(cls, status):
        return status in cls.STARTING_STATUS

    @classmethod
    def is_running(cls, status):
        return status in cls.RUNNING_STATUS

    @classmethod
    def is_deletable(cls, status):
        return not cls.is_done(status)

    @classmethod
    def is_done(cls, status):
        return status in cls.DONE_STATUS


class ExperimentLifeCycle(object):
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
    CREATED = 'Created'
    BUILDING = 'Building'
    SCHEDULED = 'Scheduled'
    STARTING = 'Starting'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    STOPPED = 'Stopped'
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (BUILDING, BUILDING),
        (SCHEDULED, SCHEDULED),
        (STARTING, STARTING),
        (RUNNING, RUNNING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
        (STOPPED, STOPPED),
        (UNKNOWN, UNKNOWN),
    )

    RUNNING_STATUS = [SCHEDULED, BUILDING, STARTING, RUNNING]
    DONE_STATUS = [FAILED, STOPPED, SUCCEEDED]

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

    @staticmethod
    def jobs_deletable(job_statuses):
        return all([True if JobLifeCycle.is_deletable(job_status) else False
                    for job_status in job_statuses])

    @classmethod
    def is_running(cls, status):
        return status in cls.RUNNING_STATUS

    @classmethod
    def is_done(cls, status):
        return status in cls.DONE_STATUS

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
