import pytest

from db.redis.heartbeat import RedisHeartBeat
from tests.utils import BaseTest


@pytest.mark.redis_mark
class TestRedisHeartBeat(BaseTest):
    def test_redis_heartbeat_raises_for_wrong_values(self):
        with self.assertRaises(ValueError):
            RedisHeartBeat(experiment=1, job=1)

        with self.assertRaises(ValueError):
            RedisHeartBeat(job=1, build=1)

        with self.assertRaises(ValueError):
            RedisHeartBeat(experiment=1, job=1, build=1)

        with self.assertRaises(ValueError):
            RedisHeartBeat()

    def test_redis_heartbeat_experiment(self):
        heartbeat = RedisHeartBeat(experiment=1)
        self.assertEqual(heartbeat.redis_key, RedisHeartBeat.KEY_EXPERIMENT.format(1))
        self.assertEqual(heartbeat.is_alive(), False)
        self.assertEqual(RedisHeartBeat.experiment_is_alive(1), False)

        heartbeat.ping()
        self.assertEqual(heartbeat.is_alive(), True)
        self.assertEqual(RedisHeartBeat.experiment_is_alive(1), True)

        heartbeat.clear()
        self.assertEqual(heartbeat.is_alive(), False)
        self.assertEqual(RedisHeartBeat.experiment_is_alive(1), False)

        RedisHeartBeat.experiment_ping(1)
        self.assertEqual(heartbeat.is_alive(), True)
        self.assertEqual(RedisHeartBeat.experiment_is_alive(1), True)

    def test_redis_heartbeat_job(self):
        heartbeat = RedisHeartBeat(job=1)
        self.assertEqual(heartbeat.redis_key, RedisHeartBeat.KEY_JOB.format(1))
        self.assertEqual(heartbeat.is_alive(), False)
        self.assertEqual(RedisHeartBeat.job_is_alive(1), False)

        heartbeat.ping()
        self.assertEqual(heartbeat.is_alive(), True)
        self.assertEqual(RedisHeartBeat.job_is_alive(1), True)

        heartbeat.clear()
        self.assertEqual(heartbeat.is_alive(), False)
        self.assertEqual(RedisHeartBeat.job_is_alive(1), False)

        RedisHeartBeat.job_ping(1)
        self.assertEqual(heartbeat.is_alive(), True)
        self.assertEqual(RedisHeartBeat.job_is_alive(1), True)

    def test_redis_heartbeat_build(self):
        heartbeat = RedisHeartBeat(build=1)
        self.assertEqual(heartbeat.redis_key, RedisHeartBeat.KEY_BUILD.format(1))
        self.assertEqual(heartbeat.is_alive(), False)
        self.assertEqual(RedisHeartBeat.build_is_alive(1), False)

        heartbeat.ping()
        self.assertEqual(heartbeat.is_alive(), True)
        self.assertEqual(RedisHeartBeat.build_is_alive(1), True)

        heartbeat.clear()
        self.assertEqual(heartbeat.is_alive(), False)
        self.assertEqual(RedisHeartBeat.build_is_alive(1), False)

        RedisHeartBeat.build_ping(1)
        self.assertEqual(heartbeat.is_alive(), True)
        self.assertEqual(RedisHeartBeat.build_is_alive(1), True)
