from typing import List, Optional, Tuple

from db.redis.base import BaseRedisDb
from polyaxon.settings import RedisPools


class RedisJobContainers(BaseRedisDb):
    """
    Tracks containers currently running and to be monitored.
    """

    KEY_CONTAINERS = 'CONTAINERS'  # Redis set: container ids
    KEY_CONTAINERS_TO_JOBS = 'CONTAINERS_TO_JOBS'  # Redis hash, maps container id to jobs
    KEY_JOBS_TO_CONTAINERS = 'JOBS_TO_CONTAINERS:{}'  # Redis set, maps jobs to containers
    KEY_JOBS_TO_EXPERIMENTS = 'JOBS_TO_EXPERIMENTS:'  # Redis hash, maps jobs to experiments

    REDIS_POOL = RedisPools.JOB_CONTAINERS

    @classmethod
    def get_containers(cls) -> List[str]:
        red = cls._get_redis()
        container_ids = red.smembers(cls.KEY_CONTAINERS)
        return [container_id.decode('utf-8') for container_id in container_ids]

    @classmethod
    def get_experiment_for_job(cls, job_uuid: str, red=None) -> Optional[str]:
        red = red or cls._get_redis()
        experiment_uuid = red.hget(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid)
        return experiment_uuid.decode('utf-8') if experiment_uuid else None

    @classmethod
    def get_job(cls, container_id: str) -> Tuple[Optional[str], Optional[str]]:
        red = cls._get_redis()
        if red.sismember(cls.KEY_CONTAINERS, container_id):
            job_uuid = red.hget(cls.KEY_CONTAINERS_TO_JOBS, container_id)
            if not job_uuid:
                return None, None

            job_uuid = job_uuid.decode('utf-8')
            experiment_uuid = cls.get_experiment_for_job(job_uuid=job_uuid, red=red)
            return job_uuid, experiment_uuid
        return None, None

    @classmethod
    def remove_container(cls, container_id: str, red=None) -> None:
        red = red or cls._get_redis()
        red.srem(cls.KEY_CONTAINERS, container_id)
        red.hdel(cls.KEY_CONTAINERS_TO_JOBS, container_id)

    @classmethod
    def remove_job(cls, job_uuid: str) -> None:
        red = cls._get_redis()
        key_jobs_to_containers = cls.KEY_JOBS_TO_CONTAINERS.format(job_uuid)
        containers = red.smembers(key_jobs_to_containers)
        for container_id in containers:
            container_id = container_id.decode('utf-8')
            red.srem(key_jobs_to_containers, container_id)
            cls.remove_container(container_id=container_id, red=red)

        # Remove the experiment too
        red.hdel(cls.KEY_CONTAINERS_TO_JOBS, job_uuid)

    @classmethod
    def monitor(cls, container_id: str, job_uuid: str) -> None:
        red = cls._get_redis()
        if not red.sismember(cls.KEY_CONTAINERS, container_id):
            from db.models.experiment_jobs import ExperimentJob

            try:
                job = ExperimentJob.objects.get(uuid=job_uuid)
            except ExperimentJob.DoesNotExist:
                return

            red.sadd(cls.KEY_CONTAINERS, container_id)
            red.hset(cls.KEY_CONTAINERS_TO_JOBS, container_id, job_uuid)
            # Add container for job
            red.sadd(cls.KEY_JOBS_TO_CONTAINERS.format(job_uuid), container_id)
            # Add job to experiment
            red.hset(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid, job.experiment.uuid.hex)
