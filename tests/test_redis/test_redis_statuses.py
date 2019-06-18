import pytest

from db.redis.statuses import RedisStatuses
from tests.base.case import BaseTest


@pytest.mark.redis_mark
class TestRedisStatuses(BaseTest):
    def test_keys(self):
        assert RedisStatuses.get_status_key('foo') == RedisStatuses.KEY_STATUSES.format('foo')

    def test_status_change(self):
        assert RedisStatuses.get_status('job-uuid') is None
        RedisStatuses.delete_status('job-uuid')
        RedisStatuses.set_status('job-uuid', 'running')
        assert RedisStatuses.get_status('job-uuid') == 'running'
        RedisStatuses.delete_status('job-uuid')
        assert RedisStatuses.get_status('job-uuid') is None
