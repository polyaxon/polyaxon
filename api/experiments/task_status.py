# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.settings import RedisPools
from libs.task_status import BaseJobStatus


class ExperimentStatus(BaseJobStatus):
    """The `ExperimentStatus` class holds information about the experiment run status.

    In order to get the status of an experiment, we store the last celery job_id for
    the given experiment id.
    """

    REDIS_OBJECTS_KEY = 'EXPERIMENTS'
    REDIS_JOBS_KEY = 'EXPERIMENTS_JOBS'
    REDIS_POOL = RedisPools.JOB_STATUS
