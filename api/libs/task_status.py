# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import redis

from celery.result import AsyncResult


class BaseJobStatus(object):
    """The `BaseJobStatus` is an abstract class holding information about an object run status.

    In order to get the run status, we store the last celery job_id for the given object id.
    And then map the job id to the status.
    """

    __metaclass__ = abc.ABCMeta

    REDIS_OBJECTS_KEY = None  # A hash mapping object_id to job_id
    REDIS_JOBS_KEY = None  # A hash mapping a job_id to status
    REDIS_POOL = None  # The redis pool where we should store data.

    @classmethod
    def _get_redis(cls):
        assert cls.REDIS_OBJECTS_KEY is not None, 'Arg `REDIS_OBJECTS_KEY` must be set.'
        assert cls.REDIS_JOBS_KEY is not None, 'Arg `REDIS_JOBS_KEY` must be set.'
        assert cls.REDIS_POOL is not None, 'Arg `REDIS_POOL` must be set.'
        return redis.Redis(connection_pool=cls.REDIS_POOL)

    @staticmethod
    def is_final_status(status):
        """Returns True if the status is final and won't be updated."""
        return status in ['SUCCESS', 'FAILURE']

    @classmethod
    def get_status(cls, object_id):
        """Return the status for an experiment given the id."""
        red = cls._get_redis()
        job_id = red.hget(cls.REDIS_OBJECTS_KEY, object_id)
        if job_id:
            job_status = red.hget(cls.REDIS_JOBS_KEY, job_id)
            if job_status is None or cls.is_final_status(job_status):
                return job_id, job_status

            # The status is not final, we need to check celery and check if the status changed.
            new_job_status = AsyncResult(job_id).state
            if new_job_status != job_status:
                cls.set_job_status(job_id=job_id, status=new_job_status)

            return job_id, new_job_status
        return None, None

    @classmethod
    def set_object_job(cls, object_id, job_id):
        red = cls._get_redis()
        red.hset(cls.REDIS_OBJECTS_KEY, object_id, job_id)

    @classmethod
    def set_job_status(cls, job_id, status):
        red = cls._get_redis()
        red.hset(cls.REDIS_JOBS_KEY, job_id, status)

    @classmethod
    def set_status(cls, object_id, job_id, status):
        cls.set_object_job(object_id=object_id, job_id=job_id)
        cls.set_job_status(job_id=job_id, status=status)
