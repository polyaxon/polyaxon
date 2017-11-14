# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.settings import RedisPools, redis
from experiments.constants import ExperimentLifeCycle
from experiments.models import ExperimentStatus, ExperimentJobStatus


class RedisExperimentStatus(object):
    """The `ExperimentStatus` class holds information about the experiment run status."""

    REDIS_EXPERIMENTS_KEY = 'EXPERIMENTS'  # Redis set: experiments to monitor the status
    REDIS_EXPERIMENTS_STATUS_KEY = 'EXPERIMENTS_STATUS'  # Redis Hash: maps experiments to status
    REDIS_POOL = RedisPools.EXPERIMENTS_STATUS  # Redis pool

    @classmethod
    def _get_redis(cls):
        return redis.Redis(connection_pool=cls.REDIS_POOL)

    @classmethod
    def get_status(cls, object_id):
        """Return the status for an experiment given the id."""
        red = cls._get_redis()
        if red.sismember(cls.REDIS_EXPERIMENTS_KEY, object_id):
            status = red.hget(cls.REDIS_EXPERIMENTS_STATUS_KEY, object_id)
            return status

    @classmethod
    def set_status(cls, object_id, status):
        red = cls._get_redis()
        current_status = cls.get_status(object_id=object_id)
        if status != current_status:
            red.hset(cls.REDIS_EXPERIMENTS_STATUS_KEY, object_id, status)
            # Add new status to the experiment
            ExperimentStatus.objects.create(experiment_id=object_id, status=status)
            # Check if we need to remove this experiment from the set to monitor
            if ExperimentLifeCycle.is_done(status):
                red.srem(cls.REDIS_EXPERIMENTS_KEY, object_id)
            return True
        return False

    @classmethod
    def monitor(cls, object_id):
        red = cls._get_redis()
        red.sadd(cls.REDIS_EXPERIMENTS_KEY, object_id)


class RedisExperimentJobStatus(object):
    """The `RedisExperimentJobStatus` class holds information about the experiment run status."""

    REDIS_JOBS_KEY = 'JOBS'  # Redis set: jobs to monitor the status
    REDIS_JOBS_STATUS_KEY = 'JOBS_STATUS'  # Redis Hash: maps jobs to status
    REDIS_JOBS_TO_EXPERIMENTS = 'JOBS_TO_EXPERIMENTS'  # Redis hash, maps jobs to experiments
    REDIS_POOL = RedisPools.JOBS_STATUS  # Redis pool

    @classmethod
    def _get_redis(cls):
        return redis.Redis(connection_pool=cls.REDIS_POOL)

    @classmethod
    def get_status(cls, object_id):
        """Return the status for an job given the id."""
        red = cls._get_redis()
        if red.sismember(cls.REDIS_JOBS_KEY, object_id):
            status = red.hget(cls.REDIS_JOBS_STATUS_KEY, object_id)
            return status

    @classmethod
    def get_experiment(cls, object_id):
        red = cls._get_redis()
        return red.hget(cls.REDIS_JOBS_TO_EXPERIMENTS, object_id)

    @classmethod
    def set_status(cls, object_id, status, message=None):
        red = cls._get_redis()
        current_status = cls.get_status(object_id=object_id)
        if status != current_status:
            red.hset(cls.REDIS_JOBS_STATUS_KEY, object_id, status)
            # Add new status to the job
            ExperimentJobStatus.objects.create(job_id=object_id, status=status, message=message)
            # Check if we need to remove this job from the set to monitor
            if ExperimentLifeCycle.is_done(status):
                red.srem(cls.REDIS_JOBS_KEY, object_id)
            return True
        return False

    @classmethod
    def monitor(cls, object_id):
        red = cls._get_redis()
        red.sadd(cls.REDIS_JOBS_KEY, object_id)
