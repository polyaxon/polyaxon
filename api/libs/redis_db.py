# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


from api.settings import RedisPools, redis
from experiments.models import ExperimentStatus, ExperimentJobStatus, Experiment, ExperimentJob
from spawner.utils.constants import JobLifeCycle, ExperimentLifeCycle


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
    def get_status(cls, experiment_uuid):
        """Return the status for an experiment given the id."""
        red = cls._get_redis()
        if red.sismember(cls.KEY_EXPERIMENTS, experiment_uuid):
            status = red.hget(cls.KEY_EXPERIMENTS_STATUS, experiment_uuid)
            return status

    @classmethod
    def set_status(cls, experiment_uuid, status):
        red = cls._get_redis()
        current_status = cls.get_status(experiment_uuid=experiment_uuid)
        if status != current_status:
            red.hset(cls.KEY_EXPERIMENTS_STATUS, experiment_uuid, status)
            # Add new status to the experiment
            experiment = Experiment.objects.get(uuid=experiment_uuid)
            ExperimentStatus.objects.create(experiment=experiment, status=status)
            # Check if we need to remove this experiment from the set to monitor
            if ExperimentLifeCycle.is_done(status):
                red.srem(cls.KEY_EXPERIMENTS, experiment_uuid)
            return True
        return False

    @classmethod
    def monitor(cls, experiment_uuid):
        red = cls._get_redis()
        red.sadd(cls.KEY_EXPERIMENTS, experiment_uuid)


class RedisExperimentJobStatus(BaseRedisDb):
    """The `RedisExperimentJobStatus` class holds information about the job run status."""

    KEY_JOBS = 'JOBS'  # Redis set: jobs to monitor the status
    KEY_JOBS_STATUS = 'JOBS_STATUS'  # Redis Hash: maps jobs to status
    KEY_JOBS_TO_EXPERIMENTS = 'JOBS_TO_EXPERIMENTS'  # Redis hash, maps jobs to experiments
    KEYF_JOBS_TO_CONTAINERS = 'JOBS_TO_CONTAINERS:{}'  # Redis set, maps jobs to containers

    REDIS_POOL = RedisPools.JOBS_STATUS  # Redis pool

    @classmethod
    def get_status(cls, job_uuid):
        """Return the status for an job given the id."""
        red = cls._get_redis()
        if red.sismember(cls.KEY_JOBS, job_uuid):
            status = red.hget(cls.KEY_JOBS_STATUS, job_uuid)
            return status.decode('utf-8')

    @classmethod
    def get_experiment(cls, job_uuid):
        red = cls._get_redis()
        experiment_uuid = red.hget(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid)
        return experiment_uuid.decode('utf-8') if experiment_uuid else None

    @classmethod
    def set_status(cls, job_uuid, status, message=None, details=None):
        red = cls._get_redis()
        current_status = cls.get_status(job_uuid=job_uuid)
        if status != current_status:
            red.hset(cls.KEY_JOBS_STATUS, job_uuid, status)
            # Add new status to the job
            job = ExperimentJob.objects.get(uuid=job_uuid)
            ExperimentJobStatus.objects.create(job=job,
                                               status=status,
                                               message=message,
                                               details=details)
            # Check if we need to remove this job from the set to monitor
            if JobLifeCycle.is_done(status):
                red.srem(cls.KEY_JOBS, job_uuid)
                # we need also to remove containers monitoring related to the job
                key_jobs_to_containers = cls.KEYF_JOBS_TO_CONTAINERS.format(job_uuid)
                containers = red.sismember(key_jobs_to_containers, job_uuid)
                for container_id in containers:
                    container_id = container_id.decode('utf-8')
                    red.srem(key_jobs_to_containers, container_id)
                    RedisJobContainers.remove_container(container_id=container_id)
            return True
        return False

    @classmethod
    def add_container_for_job(cls, job_uuid, container_id):
        red = cls._get_redis()
        red.sadd(cls.KEYF_JOBS_TO_CONTAINERS.format(job_uuid), container_id)

    @classmethod
    def monitor(cls, job_uuid, experiment_uuid):
        red = cls._get_redis()
        red.sadd(cls.KEY_JOBS, job_uuid)
        red.hset(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid, experiment_uuid)


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
    def get_job(cls, container_id):
        red = cls._get_redis()
        job_uuid = None
        if red.sismember(cls.KEY_CONTAINERS, container_id):
            job_uuid = red.hget(cls.KEY_CONTAINERS_TO_JOBS, container_id)
        return job_uuid.decode('utf-8') if job_uuid else None

    @classmethod
    def monitor(cls, container_id, job_uuid):
        red = cls._get_redis()
        red.sadd(cls.KEY_CONTAINERS, container_id)
        red.hset(cls.KEY_CONTAINERS_TO_JOBS, container_id, job_uuid)
        RedisExperimentJobStatus.add_container_for_job(job_uuid=job_uuid, container_id=container_id)

    @classmethod
    def remove_container(cls, container_id):
        red = cls._get_redis()
        red.srem(cls.KEY_CONTAINERS, container_id)
        red.hdel(cls.KEY_CONTAINERS_TO_JOBS, container_id)


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
    def monitor_job_resources(cls, job_uuid):
        cls._monitor(cls.KEY_JOB_RESOURCES, job_uuid)

    @classmethod
    def monitor_job_logs(cls, job_uuid):
        cls._monitor(cls.KEY_JOB_LOGS, job_uuid)

    @classmethod
    def monitor_experiment_resources(cls, experiment_uuid):
        cls._monitor(cls.KEY_EXPERIMENT_RESOURCES, experiment_uuid)

    @classmethod
    def monitor_experiment_logs(cls, experiment_uuid):
        cls._monitor(cls.KEY_EXPERIMENT_LOGS, experiment_uuid)

    @classmethod
    def _is_monitored(cls, key, object_id):
        red = cls._get_redis()
        return red.sismember(key, object_id)

    @classmethod
    def is_monitored_job_resources(cls, job_uuid):
        return cls._is_monitored(cls.KEY_JOB_RESOURCES, job_uuid)

    @classmethod
    def is_monitored_job_logs(cls, job_uuid):
        return cls._is_monitored(cls.KEY_JOB_LOGS, job_uuid)

    @classmethod
    def is_monitored_experiment_resources(cls, experiment_uuid):
        return cls._is_monitored(cls.KEY_EXPERIMENT_RESOURCES, experiment_uuid)

    @classmethod
    def is_monitored_experiment_logs(cls, experiment_uuid):
        return cls._is_monitored(cls.KEY_EXPERIMENT_LOGS, experiment_uuid)

    @classmethod
    def _remove_object(cls, key, object_id):
        red = cls._get_redis()
        red.srem(key, object_id)

    @classmethod
    def remove_job_resources(cls, job_uuid):
        cls._remove_object(cls.KEY_JOB_RESOURCES, job_uuid)

    @classmethod
    def remove_job_logs(cls, job_uuid):
        cls._remove_object(cls.KEY_JOB_LOGS, job_uuid)

    @classmethod
    def remove_experiment_resources(cls, experiment_uuid):
        cls._remove_object(cls.KEY_EXPERIMENT_RESOURCES, experiment_uuid)

    @classmethod
    def remove_experiment_logs(cls, experiment_uuid):
        cls._remove_object(cls.KEY_EXPERIMENT_LOGS, experiment_uuid)

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
