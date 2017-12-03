# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_k8s.constants import JobLifeCycle, ExperimentLifeCycle

from api.settings import RedisPools, redis
from experiments.models import ExperimentStatus, ExperimentJobStatus


class BaseRedisDb(object):
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls):
        return redis.Redis(connection_pool=cls.REDIS_POOL)


class RedisExperimentStatus(BaseRedisDb):
    """The `ExperimentStatus` class holds information about the experiment run status."""

    KEY_EXPERIMENTS = 'EXPERIMENTS'  # Redis set: experiments to monitor the status
    KEY_EXPERIMENTS_STATUS = 'EXPERIMENTS_STATUS'  # Redis Hash: maps experiments to status
    REDIS_POOL = RedisPools.EXPERIMENTS_STATUS  # Redis pool

    @classmethod
    def get_status(cls, object_id):
        """Return the status for an experiment given the id."""
        red = cls._get_redis()
        if red.sismember(cls.KEY_EXPERIMENTS, object_id):
            status = red.hget(cls.KEY_EXPERIMENTS_STATUS, object_id)
            return status

    @classmethod
    def set_status(cls, object_id, status):
        red = cls._get_redis()
        current_status = cls.get_status(object_id=object_id)
        if status != current_status:
            red.hset(cls.KEY_EXPERIMENTS_STATUS, object_id, status)
            # Add new status to the experiment
            ExperimentStatus.objects.create(experiment_id=object_id, status=status)
            # Check if we need to remove this experiment from the set to monitor
            if ExperimentLifeCycle.is_done(status):
                red.srem(cls.KEY_EXPERIMENTS, object_id)
            return True
        return False

    @classmethod
    def monitor(cls, object_id):
        red = cls._get_redis()
        red.sadd(cls.KEY_EXPERIMENTS, object_id)


class RedisExperimentJobStatus(BaseRedisDb):
    """The `RedisExperimentJobStatus` class holds information about the job run status."""

    KEY_JOBS = 'JOBS'  # Redis set: jobs to monitor the status
    KEY_JOBS_STATUS = 'JOBS_STATUS'  # Redis Hash: maps jobs to status
    KEY_JOBS_TO_EXPERIMENTS = 'JOBS_TO_EXPERIMENTS'  # Redis hash, maps jobs to experiments
    REDIS_POOL = RedisPools.JOBS_STATUS  # Redis pool

    @classmethod
    def get_status(cls, object_id):
        """Return the status for an job given the id."""
        red = cls._get_redis()
        if red.sismember(cls.KEY_JOBS, object_id):
            status = red.hget(cls.KEY_JOBS_STATUS, object_id)
            return status

    @classmethod
    def get_experiment(cls, object_id):
        red = cls._get_redis()
        return red.hget(cls.KEY_JOBS_TO_EXPERIMENTS, object_id)

    @classmethod
    def set_status(cls, object_id, status, message=None, details=None):
        red = cls._get_redis()
        current_status = cls.get_status(object_id=object_id)
        if status != current_status:
            red.hset(cls.KEY_JOBS_STATUS, object_id, status)
            # Add new status to the job
            ExperimentJobStatus.objects.create(job_id=object_id,
                                               status=status,
                                               message=message,
                                               details=details)
            # Check if we need to remove this job from the set to monitor
            if JobLifeCycle.is_done(status):
                red.srem(cls.KEY_JOBS, object_id)
                check_experiment_status.delay(experiment_id)
            return True
        return False

    @classmethod
    def monitor(cls, object_id):
        red = cls._get_redis()
        red.sadd(cls.KEY_JOBS, object_id)


class RedisJobContainers(BaseRedisDb):
    """Tracks containers currently running and to be monitored."""

    KEY_CONTAINERS = 'CONTAINERS'  # Redis set: container ids
    KEY_CONTAINERS_TO_JOBS = 'CONTAINERS_TO_JOBS'  # Redis hash, maps container id to jobs

    REDIS_POOL = RedisPools.JOB_CONTAINERS

    @classmethod
    def get_containers(cls):
        red = cls._get_redis()
        container_ids = red.smembers(cls.KEY_CONTAINERS)
        return [container_id.decode('utf-8') for container_id in container_ids]

    @classmethod
    def get_job(cls, object_id):
        red = cls._get_redis()
        job_id = None
        if red.sismember(cls.KEY_CONTAINERS, object_id):
            job_id = red.hget(cls.KEY_CONTAINERS_TO_JOBS, object_id)
        return job_id.decode('utf-8') if job_id else None

    @classmethod
    def monitor(cls, object_id, job_id):
        red = cls._get_redis()
        red.sadd(cls.KEY_CONTAINERS, object_id)
        red.hset(cls.KEY_CONTAINERS_TO_JOBS, object_id, job_id)

    @classmethod
    def remove_container(cls, object_id):
        red = cls._get_redis()
        red.srem(cls.KEY_CONTAINERS, object_id)
        red.hdel(cls.KEY_CONTAINERS_TO_JOBS, object_id)


class RedisToStream(BaseRedisDb):
    """Tracks resources and logs,  currently running and to be monitored."""

    KEY_JOB_RESOURCES = 'JOB_RESOURCES'  # Redis set: job ids that we need to stream resources for
    KEY_EXPERIMENT_RESOURCES = 'EXPERIMENT_RESOURCES'  # Redis set: xp ids that
    # we need to stream resources for
    KEY_JOB_LOGS = 'JOB_LOGS'  # Redis set: job ids that we need to stream logs for
    KEY_EXPERIMENT_LOGS = 'EXPERIMENT_LOGS'  # Redis set: xp ids that we need to stream logs for
    KEY_JOB_LATEST_STATS = 'JOB_LATEST_STATS'  # Redis hash, maps job id to dict of stats
    # We don't need a key for experiment because we will just aggregate jobs' stats
    # N.B: for logs, since we need to send all data since the tracking we will publish the data
    # Through an exchange

    REDIS_POOL = RedisPools.JOB_CONTAINERS

    @classmethod
    def _monitor(cls, key, object_id):
        red = cls._get_redis()
        red.sadd(key, object_id)

    @classmethod
    def monitor_job_resources(cls, job):
        cls._monitor(cls.KEY_JOB_RESOURCES, job)

    @classmethod
    def monitor_job_logs(cls, job):
        cls._monitor(cls.KEY_JOB_LOGS, job)

    @classmethod
    def monitor_experiment_resources(cls, experiment):
        cls._monitor(cls.KEY_EXPERIMENT_RESOURCES, experiment)

    @classmethod
    def monitor_experiment_logs(cls, experiment):
        cls._monitor(cls.KEY_EXPERIMENT_LOGS, experiment)

    @classmethod
    def _is_monitored(cls, key, object_id):
        red = cls._get_redis()
        return red.sismember(key, object_id)

    @classmethod
    def is_monitored_job_resources(cls, job):
        return cls._is_monitored(cls.KEY_JOB_RESOURCES, job)

    @classmethod
    def is_monitored_job_logs(cls, job):
        return cls._is_monitored(cls.KEY_JOB_LOGS, job)

    @classmethod
    def is_monitored_experiment_resources(cls, experiment):
        return cls._is_monitored(cls.KEY_EXPERIMENT_RESOURCES, experiment)

    @classmethod
    def is_monitored_experiment_logs(cls, experiment):
        return cls._is_monitored(cls.KEY_EXPERIMENT_LOGS, experiment)

    @classmethod
    def _remove_object(cls, key, object_id):
        red = cls._get_redis()
        red.srem(key, object_id)

    @classmethod
    def remove_job_resources(cls, job):
        cls._remove_object(cls.KEY_JOB_RESOURCES, job)

    @classmethod
    def remove_job_logs(cls, job):
        cls._remove_object(cls.KEY_JOB_LOGS, job)

    @classmethod
    def remove_experiment_resources(cls, experiment):
        cls._remove_object(cls.KEY_EXPERIMENT_RESOURCES, experiment)

    @classmethod
    def remove_experiment_logs(cls, experiment):
        cls._remove_object(cls.KEY_EXPERIMENT_LOGS, experiment)

    @classmethod
    def get_latest_job_resources(cls, job):
        red = cls._get_redis()
        key = '{}:{}'.format(cls.KEY_JOB_LATEST_STATS, job)
        return red.hgetall(key)

    @classmethod
    def get_latest_experiment_resources(cls, jobs):
        stats = []
        for job in jobs:
            stats.append(cls.get_latest_job_resources(job))
        return stats

    @classmethod
    def set_latest_job_resources(cls, job, payload):
        red = cls._get_redis()
        key = '{}:{}'.format(cls.KEY_JOB_LATEST_STATS, job)
        red.hmset(key, payload)
