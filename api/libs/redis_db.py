# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.settings import RedisPools, redis


class BaseRedisDb(object):
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls):
        return redis.Redis(connection_pool=cls.REDIS_POOL)


class RedisJobContainers(BaseRedisDb):
    """Tracks containers currently running and to be monitored."""

    KEY_CONTAINERS = 'CONTAINERS'  # Redis set: container ids
    KEY_CONTAINERS_TO_JOBS = 'CONTAINERS_TO_JOBS'  # Redis hash, maps container id to jobs
    KEYF_JOBS_TO_CONTAINERS = 'JOBS_TO_CONTAINERS:{}'  # Redis set, maps jobs to containers
    KEY_JOBS_TO_EXPERIMENTS = 'JOBS_TO_EXPERIMENTS:'  # Redis hash, maps jobs to experiments

    REDIS_POOL = RedisPools.JOB_CONTAINERS

    @classmethod
    def get_containers(cls):
        red = cls._get_redis()
        container_ids = red.smembers(cls.KEY_CONTAINERS)
        return [container_id.decode('utf-8') for container_id in container_ids]

    @classmethod
    def get_job(cls, container_id):
        red = cls._get_redis()
        if red.sismember(cls.KEY_CONTAINERS, container_id):
            job_uuid = red.hget(cls.KEY_CONTAINERS_TO_JOBS, container_id)
            if not job_uuid:
                return None, None

            job_uuid = job_uuid.decode('utf-8')
            experiment_uuid = red.hget(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid)
            experiment_uuid = experiment_uuid.decode('utf-8') if experiment_uuid else None
            return job_uuid, experiment_uuid
        return None, None

    @classmethod
    def remove_container(cls, container_id):
        red = cls._get_redis()
        red.srem(cls.KEY_CONTAINERS, container_id)
        red.hdel(cls.KEY_CONTAINERS_TO_JOBS, container_id)

    @classmethod
    def remove_job(cls, job_uuid):
        red = cls._get_redis()
        key_jobs_to_containers = cls.KEYF_JOBS_TO_CONTAINERS.format(job_uuid)
        containers = red.smembers(key_jobs_to_containers)
        for container_id in containers:
            container_id = container_id.decode('utf-8')
            red.srem(key_jobs_to_containers, container_id)
            cls.remove_container(container_id=container_id)

        # Remove the experiment too
        red.hdel(cls.KEY_CONTAINERS_TO_JOBS, job_uuid)

    @classmethod
    def monitor(cls, container_id, job_uuid):
        red = cls._get_redis()
        if not red.sismember(cls.KEY_CONTAINERS, container_id):
            from experiments.models import ExperimentJob

            try:
                job = ExperimentJob.objects.get(uuid=job_uuid)
            except ExperimentJob.DoesNotExist:
                return

            red.sadd(cls.KEY_CONTAINERS, container_id)
            red.hset(cls.KEY_CONTAINERS_TO_JOBS, container_id, job_uuid)
            # Add container for job
            red.sadd(cls.KEYF_JOBS_TO_CONTAINERS.format(job_uuid), container_id)
            # Add job to experiment
            red.hset(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid, job.experiment.uuid.hex)


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
        red.hmset(key, payload.to_dict())
