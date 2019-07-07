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

    def __init__(self):
        self._red = self._get_redis()

    @property
    def red(self):
        return self._red

    def get_containers(self) -> List[str]:
        container_ids = self.red.smembers(self.KEY_CONTAINERS)
        return [container_id.decode('utf-8') for container_id in container_ids]

    def get_experiment_for_job(self, job_uuid: str, red=None) -> Optional[str]:
        red = red or self.red
        experiment_uuid = red.hget(self.KEY_JOBS_TO_EXPERIMENTS, job_uuid)
        return experiment_uuid.decode('utf-8') if experiment_uuid else None

    def get_job(self, container_id: str) -> Tuple[Optional[str], Optional[str]]:
        if self.red.sismember(self.KEY_CONTAINERS, container_id):
            job_uuid = self.red.hget(self.KEY_CONTAINERS_TO_JOBS, container_id)
            if not job_uuid:
                return None, None

            job_uuid = job_uuid.decode('utf-8')
            experiment_uuid = self.get_experiment_for_job(job_uuid=job_uuid)
            return job_uuid, experiment_uuid
        return None, None

    def remove_container(self, container_id: str, red=None) -> None:
        red = red or self.red
        red.srem(self.KEY_CONTAINERS, container_id)
        red.hdel(self.KEY_CONTAINERS_TO_JOBS, container_id)

    def remove_job(self, job_uuid: str) -> None:
        key_jobs_to_containers = self.KEY_JOBS_TO_CONTAINERS.format(job_uuid)
        containers = self.red.smembers(key_jobs_to_containers)
        for container_id in containers:
            container_id = container_id.decode('utf-8')
            self.red.srem(key_jobs_to_containers, container_id)
            self.remove_container(container_id=container_id)

        # Remove the experiment too
        self.red.hdel(self.KEY_CONTAINERS_TO_JOBS, job_uuid)

    def monitor(self, container_id: str, job_uuid: str) -> None:
        if not self.red.sismember(self.KEY_CONTAINERS, container_id):
            from db.models.experiment_jobs import ExperimentJob

            try:
                job = ExperimentJob.objects.get(uuid=job_uuid)
            except ExperimentJob.DoesNotExist:
                return

            self.red.sadd(self.KEY_CONTAINERS, container_id)
            self.red.hset(self.KEY_CONTAINERS_TO_JOBS, container_id, job_uuid)
            # Add container for job
            self.red.sadd(self.KEY_JOBS_TO_CONTAINERS.format(job_uuid), container_id)
            # Add job to experiment
            self.red.hset(self.KEY_JOBS_TO_EXPERIMENTS, job_uuid, job.experiment.uuid.hex)
