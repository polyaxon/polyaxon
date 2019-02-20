import pytest

import conf

from db.redis.tll import RedisTTL
from tests.utils import BaseTest


@pytest.mark.redis_mark
class TestRedisTTL(BaseTest):
    def test_redis_ttl_raises_for_wrong_values(self):
        with self.assertRaises(ValueError):
            RedisTTL(experiment=1, job=1)

        with self.assertRaises(ValueError):
            RedisTTL(job=1, build=1)

        with self.assertRaises(ValueError):
            RedisTTL(experiment=1, job=1, build=1)

        with self.assertRaises(ValueError):
            RedisTTL()

    def test_redis_ttl_experiment(self):
        ttl = RedisTTL(experiment=1)
        assert ttl.redis_key == RedisTTL.KEY_EXPERIMENT.format(1)

        ttl.set_value(10)
        assert ttl.get_value() == 10

        ttl.set_value(13)
        assert ttl.get_value() == 13

        ttl.clear()

        assert ttl.get_value() is None

    def test_set_for_experiment(self):
        RedisTTL.set_for_experiment(experiment_id=1, value=10)
        assert RedisTTL.get_for_experiment(experiment_id=1) == 10
        assert RedisTTL.get_for_experiment(experiment_id=2) == conf.get('GLOBAL_COUNTDOWN')
        assert RedisTTL(experiment=10).get_value() is None

    def test_redis_ttl_job(self):
        ttl = RedisTTL(job=1)
        assert ttl.redis_key == RedisTTL.KEY_JOB.format(1)

        ttl.set_value(10)
        assert ttl.get_value() == 10

        ttl.set_value(13)
        assert ttl.get_value() == 13

        ttl.clear()

        assert ttl.get_value() is None

    def test_set_for_job(self):
        RedisTTL.set_for_job(job_id=1, value=10)
        assert RedisTTL.get_for_job(job_id=1) == 10
        assert RedisTTL.get_for_job(job_id=2) == conf.get('GLOBAL_COUNTDOWN')
        assert RedisTTL(job=10).get_value() is None

    def test_redis_ttl_build(self):
        ttl = RedisTTL(build=1)
        assert ttl.redis_key == RedisTTL.KEY_BUILD.format(1)

        ttl.set_value(10)
        assert ttl.get_value() == 10

        ttl.set_value(13)
        assert ttl.get_value() == 13

        ttl.clear()

        assert ttl.get_value() is None

    def test_set_for_build(self):
        RedisTTL.set_for_build(build_id=1, value=10)
        assert RedisTTL.get_for_build(build_id=1) == 10
        assert RedisTTL.get_for_build(build_id=2) == conf.get('GLOBAL_COUNTDOWN')
        assert RedisTTL(build=10).get_value() is None

    def test_validate_ttl(self):
        with self.assertRaises(ValueError):
            RedisTTL.validate_ttl(None)

        with self.assertRaises(ValueError):
            RedisTTL.validate_ttl('sdf')
