import json

from typing import Dict, List, Optional, Union

from db.redis.base import BaseRedisDb
from polyaxon.settings import RedisPools


class RedisToStream(BaseRedisDb):
    """
    Tracks resources and logs, currently running and to be monitored.
    """

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
    def _monitor(cls, key: str, object_id: str) -> None:
        red = cls._get_redis()
        red.sadd(key, object_id)

    @classmethod
    def monitor_job_resources(cls, job_uuid: str) -> None:
        cls._monitor(cls.KEY_JOB_RESOURCES, job_uuid)

    @classmethod
    def monitor_job_logs(cls, job_uuid: str) -> None:
        cls._monitor(cls.KEY_JOB_LOGS, job_uuid)

    @classmethod
    def monitor_experiment_resources(cls, experiment_uuid: str) -> None:
        cls._monitor(cls.KEY_EXPERIMENT_RESOURCES, experiment_uuid)

    @classmethod
    def monitor_experiment_logs(cls, experiment_uuid: str) -> None:
        cls._monitor(cls.KEY_EXPERIMENT_LOGS, experiment_uuid)

    @classmethod
    def _is_monitored(cls, key: str, object_id: str) -> bool:
        red = cls._get_redis()
        return red.sismember(key, object_id)

    @classmethod
    def is_monitored_job_resources(cls, job_uuid: str) -> bool:
        return cls._is_monitored(cls.KEY_JOB_RESOURCES, job_uuid)

    @classmethod
    def is_monitored_job_logs(cls, job_uuid: str) -> bool:
        return cls._is_monitored(cls.KEY_JOB_LOGS, job_uuid)

    @classmethod
    def is_monitored_experiment_resources(cls, experiment_uuid: str) -> bool:
        return cls._is_monitored(cls.KEY_EXPERIMENT_RESOURCES, experiment_uuid)

    @classmethod
    def is_monitored_experiment_logs(cls, experiment_uuid: str) -> bool:
        return cls._is_monitored(cls.KEY_EXPERIMENT_LOGS, experiment_uuid)

    @classmethod
    def _remove_object(cls, key: str, object_id: str) -> None:
        red = cls._get_redis()
        red.srem(key, object_id)

    @classmethod
    def remove_job_resources(cls, job_uuid: str) -> None:
        cls._remove_object(cls.KEY_JOB_RESOURCES, job_uuid)

    @classmethod
    def remove_job_logs(cls, job_uuid: str) -> None:
        cls._remove_object(cls.KEY_JOB_LOGS, job_uuid)

    @classmethod
    def remove_experiment_resources(cls, experiment_uuid: str) -> None:
        cls._remove_object(cls.KEY_EXPERIMENT_RESOURCES, experiment_uuid)

    @classmethod
    def remove_experiment_logs(cls, experiment_uuid: str) -> None:
        cls._remove_object(cls.KEY_EXPERIMENT_LOGS, experiment_uuid)

    @classmethod
    def get_latest_job_resources(cls,
                                 job: str,
                                 job_name: str,
                                 as_json: bool = False) -> Optional[Union[str, Dict]]:
        red = cls._get_redis()
        resources = red.hget(cls.KEY_JOB_LATEST_STATS, job)
        if resources:
            resources = resources.decode('utf-8')
            resources = json.loads(resources)
            resources['job_name'] = job_name
            return resources if as_json else json.dumps(resources)
        return None

    @classmethod
    def get_latest_experiment_resources(cls,
                                        jobs: List[Dict],
                                        as_json: bool = False) -> List[Optional[Union[str, Dict]]]:
        stats = []
        for job in jobs:
            job_resources = cls.get_latest_job_resources(job=job['uuid'],
                                                         job_name=job['name'],
                                                         as_json=True)
            if job_resources:
                stats.append(job_resources)
        return stats if as_json else json.dumps(stats)

    @classmethod
    def set_latest_job_resources(cls, job: str, payload: Dict) -> None:
        red = cls._get_redis()
        red.hset(cls.KEY_JOB_LATEST_STATS, job, json.dumps(payload))
