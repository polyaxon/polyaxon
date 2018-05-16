import json
import uuid

from libs.json_utils import dumps, loads
from polyaxon.settings import RedisPools, redis


class BaseRedisDb(object):
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls):
        return redis.Redis(connection_pool=cls.REDIS_POOL)


class RedisJobContainers(BaseRedisDb):
    """Tracks containers currently running and to be monitored."""

    KEY_CONTAINERS = 'CONTAINERS'  # Redis set: container ids
    KEY_CONTAINERS_TO_JOBS = 'CONTAINERS_TO_JOBS'  # Redis hash, maps container id to jobs
    KEY_JOBS_TO_CONTAINERS = 'JOBS_TO_CONTAINERS:{}'  # Redis set, maps jobs to containers
    KEY_JOBS_TO_EXPERIMENTS = 'JOBS_TO_EXPERIMENTS:'  # Redis hash, maps jobs to experiments

    REDIS_POOL = RedisPools.JOB_CONTAINERS

    @classmethod
    def get_containers(cls):
        red = cls._get_redis()
        container_ids = red.smembers(cls.KEY_CONTAINERS)
        return [container_id.decode('utf-8') for container_id in container_ids]

    @classmethod
    def get_experiment_for_job(cls, job_uuid, red=None):
        red = red or cls._get_redis()
        experiment_uuid = red.hget(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid)
        return experiment_uuid.decode('utf-8') if experiment_uuid else None

    @classmethod
    def get_job(cls, container_id):
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
    def remove_container(cls, container_id, red=None):
        red = red or cls._get_redis()
        red.srem(cls.KEY_CONTAINERS, container_id)
        red.hdel(cls.KEY_CONTAINERS_TO_JOBS, container_id)

    @classmethod
    def remove_job(cls, job_uuid):
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
            red.sadd(cls.KEY_JOBS_TO_CONTAINERS.format(job_uuid), container_id)
            # Add job to experiment
            red.hset(cls.KEY_JOBS_TO_EXPERIMENTS, job_uuid, job.experiment.uuid.hex)


class RedisToStream(BaseRedisDb):
    """Tracks resources and logs, currently running and to be monitored."""

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
    def get_latest_job_resources(cls, job, job_name, as_json=False):
        red = cls._get_redis()
        resources = red.hget(cls.KEY_JOB_LATEST_STATS, job)
        if resources:
            resources = resources.decode('utf-8')
            resources = json.loads(resources)
            resources['job_name'] = job_name
            return resources if as_json else json.dumps(resources)
        return None

    @classmethod
    def get_latest_experiment_resources(cls, jobs, as_json=False):
        stats = []
        for job in jobs:
            job_resources = cls.get_latest_job_resources(job=job['uuid'],
                                                         job_name=job['name'],
                                                         as_json=True)
            if job_resources:
                stats.append(job_resources)
        return stats if as_json else json.dumps(stats)

    @classmethod
    def set_latest_job_resources(cls, job, payload):
        red = cls._get_redis()
        red.hset(cls.KEY_JOB_LATEST_STATS, job, json.dumps(payload))


class RedisSessions(BaseRedisDb):
    """ RedisSessions provides a db to store data related to a request session.
    Useful for storing data too large to be stored into the session cookie.
    The session store will expire if values are not modified within the provided ttl.

    Example:
        >>> store = RedisSessions(request, 'github')
        >>> store.regenerate()
        >>> store.some_value = 'some value'

        The value will be available across requests as long as the same same store
        name is used.

        >>> store.some_value
        'my value'

        The store may be destroyed before it expires using the ``clear`` method.

        >>> store.clear()
    """
    EXPIRATION_TTL = 10 * 60
    KEY_SESSION_CACHE = 'SESSION_CACHE:{}:{}'
    KEY_SESSION_KEYS = 'SESSION_KEYS:{}'

    REDIS_POOL = RedisPools.SESSIONS

    def __init__(self, request, prefix, ttl=EXPIRATION_TTL):
        self.__dict__['request'] = request
        self.__dict__['prefix'] = prefix
        self.__dict__['ttl'] = ttl
        self.__dict__['_red'] = self._get_redis()

    @property
    def session_key(self):
        return self.KEY_SESSION_KEYS.format(self.prefix)

    @property
    def redis_key(self):
        return self.request.session.get(self.session_key)

    def regenerate(self, initial_state=None):
        if initial_state is None:
            initial_state = {}

        redis_key = self.KEY_SESSION_CACHE.format(self.prefix, uuid.uuid4().hex)

        self.request.session[self.session_key] = redis_key

        value = dumps(initial_state)
        self._red.setex(redis_key, self.ttl, value)

    def clear(self):
        if not self.redis_key:
            return

        self._red.delete(self.redis_key)
        del self.request.session[self.session_key]

    def is_valid(self):
        return self.redis_key and self._red.get(self.redis_key)

    def get_state(self):
        if not self.redis_key:
            return None

        state_json = self._red.get(self.redis_key)
        if not state_json:
            return None

        return loads(state_json)

    def __getattr__(self, key):
        state = self.get_state()

        try:
            return state[key] if state else None
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        state = self.get_state()

        if state is None:
            return

        state[key] = value
        self._red.setex(self.redis_key, self.ttl, dumps(state))
