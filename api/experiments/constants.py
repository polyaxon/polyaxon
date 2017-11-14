# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_k8s.constants import JobLifeCycle


class ExperimentLifeCycle(JobLifeCycle):
    SCHEDULED = 'Scheduled'

    CHOICES = (
        (JobLifeCycle.CREATED, JobLifeCycle.CREATED),  # XP created to be executed
        (SCHEDULED, SCHEDULED),  # XP scheduled to be started
        (JobLifeCycle.BUILDING, JobLifeCycle.BUILDING),  # XP is building containers
        (JobLifeCycle.PENDING, JobLifeCycle.PENDING),  # waiting for all jobs be ready
        (JobLifeCycle.STARTING, JobLifeCycle.STARTING),  # one of the jobs is still starting
        (JobLifeCycle.RUNNING, JobLifeCycle.RUNNING),  # one of the jobs is still running
        (JobLifeCycle.FINISHED, JobLifeCycle.FINISHED),  # master and workers have finished
        (JobLifeCycle.FAILED, JobLifeCycle.FAILED),  # one of the jobs has failed
        (JobLifeCycle.KILLED, JobLifeCycle.KILLED),  # XP was killed
    )
