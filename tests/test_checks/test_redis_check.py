import mock
import pytest
import redis

from checks.redis import RedisCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestRedisHealthCheck(BaseTest):
    def test_redis_is_healthy(self):
        results = RedisCheck.run()
        assert results['REDIS'].is_healthy is True

    @mock.patch('checks.redis.RedisToStream.connection')
    def test_connection_error(self, mocked_connection):
        mocked_conn = mock.MagicMock()
        mocked_connection.return_value = mocked_conn
        mocked_conn.info.side_effect = redis.exceptions.ConnectionError('Connection Refused')

        results = RedisCheck.run()
        assert results['REDIS_TO_STREAM'].is_healthy is False
        assert results['REDIS_TO_STREAM'].severity == Result.ERROR

    @mock.patch('checks.redis.RedisToStream.connection')
    def test_exception_raised(self, mocked_connection):
        mocked_conn = mock.MagicMock()
        mocked_connection.return_value = mocked_conn
        mocked_conn.info.side_effect = Exception('Connection Refused')

        results = RedisCheck.run()
        assert results['REDIS_TO_STREAM'].is_healthy is False
        assert results['REDIS_TO_STREAM'].severity == Result.ERROR
