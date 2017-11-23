# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_k8s.constants import JobLifeCycle


class ExperimentLifeCycle(JobLifeCycle):
    SCHEDULED = 'Scheduled'
    STARTING = 'Starting'

    CHOICES = (
        (JobLifeCycle.CREATED, JobLifeCycle.CREATED),  # XP created to be executed
        (SCHEDULED, SCHEDULED),  # XP scheduled to be started
        (STARTING, STARTING),  # one of the jobs is still not running
        (JobLifeCycle.PENDING, JobLifeCycle.PENDING),  # one of the jobs is still pending
        (JobLifeCycle.RUNNING, JobLifeCycle.RUNNING),  # one of the jobs is still running
        (JobLifeCycle.SUCCEEDED, JobLifeCycle.SUCCEEDED),  # master and workers have finished
        (JobLifeCycle.FAILED, JobLifeCycle.FAILED),  # one of the jobs has failed
        (JobLifeCycle.DELETED, JobLifeCycle.DELETED),  # XP was killed
    )
