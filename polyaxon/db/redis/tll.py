from typing import Any, Optional, Union

import conf

from db.redis.base import BaseRedisDb
from polyaxon.settings import RedisPools


class RedisTTL(BaseRedisDb):
    """
    RedisTTL provides a db to store experiment/job ttl
    before sending a signal to delete the k8s resources.
    """
    KEY_EXPERIMENT = 'ttl.experiment:{}'
    KEY_JOB = 'ttl.job:{}'
    KEY_BUILD = 'ttl.build:{}'

    TTL_KEY = 'ttl'

    REDIS_POOL = RedisPools.TTL

    def __init__(self, experiment: int = None, job: int = None, build: int = None) -> None:
        if len([1 for i in [experiment, job, build] if i]) != 1:
            raise ValueError('RedisTTL expects an experiment, build or a job.')

        self.__dict__['_is_experiment'] = False
        self.__dict__['_is_job'] = False
        self.__dict__['_is_build'] = False
        if experiment:
            self.__dict__['_is_experiment'] = True
        if job:
            self.__dict__['_is_job'] = True
        if build:
            self.__dict__['_is_build'] = True
        self.__dict__['key'] = experiment or job or build
        self.__dict__['_red'] = self._get_redis()

    def __getattr__(self, key: str) -> Any:
        value = self.get_value()

        try:
            return value
        except KeyError as e:
            raise AttributeError(e)

    def get_value(self) -> Optional[int]:
        if not self.redis_key:
            return None

        value = self._red.get(self.redis_key)
        if not value:
            return None

        return int(value.decode())

    def set_value(self, value: Union[int, str]) -> None:
        try:
            value = int(value)
        except (TypeError, ValueError):
            return None
        self._red.set(name=self.redis_key, value=value)

    @property
    def redis_key(self) -> str:
        if self._is_experiment:
            return self.KEY_EXPERIMENT.format(self.key)
        if self._is_job:
            return self.KEY_JOB.format(self.key)
        if self._is_build:
            return self.KEY_BUILD.format(self.key)
        raise KeyError('Wrong RedisTTL key')

    def clear(self) -> None:
        if not self.redis_key:
            return

        self._red.delete(self.redis_key)

    @staticmethod
    def validate_ttl(value) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError('RedisTTL expects int values.')

    @classmethod
    def set_for_experiment(cls, experiment_id: int, value: Union[int, str]) -> None:
        value = cls.validate_ttl(value)
        ttl = RedisTTL(experiment=experiment_id)
        ttl.set_value(value)

    @classmethod
    def set_for_job(cls, job_id: int, value: Union[int, str]) -> None:
        value = cls.validate_ttl(value)
        ttl = RedisTTL(job=job_id)
        ttl.set_value(value)

    @classmethod
    def set_for_build(cls, build_id: int, value: Union[int, str]) -> None:
        value = cls.validate_ttl(value)
        ttl = RedisTTL(build=build_id)
        ttl.set_value(value)

    @classmethod
    def get_for_experiment(cls, experiment_id: int) -> int:
        ttl = RedisTTL(experiment=experiment_id)
        ttl_value = ttl.get_value()
        if ttl_value:
            ttl.clear()
            return ttl_value
        return conf.get('GLOBAL_COUNTDOWN')

    @classmethod
    def get_for_job(cls, job_id: int) -> int:
        ttl = RedisTTL(job=job_id)
        ttl_value = ttl.get_value()
        if ttl_value:
            ttl.clear()
            return ttl_value
        return conf.get('GLOBAL_COUNTDOWN')

    @classmethod
    def get_for_build(cls, build_id: int) -> int:
        ttl = RedisTTL(build=build_id)
        ttl_value = ttl.get_value()
        if ttl_value:
            ttl.clear()
            return ttl_value
        return conf.get('GLOBAL_COUNTDOWN')
