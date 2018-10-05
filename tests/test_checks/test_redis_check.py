import pytest
import mock

from checks.results import Result
from tests.utils import BaseTest
from checks.postgres import PostgresCheck


@pytest.mark.checks_mark
class TestRedisHealthCheck(BaseTest):
    DISABLE_RUNNER = True

    def test_redis_is_healthy(self):
        results = PostgresCheck.run()
        assert results['REDIS'].is_healthy is True

    @mock.patch('checks.redis.RedisToStream.connection')
    def test_cursor_error(self, mocked_connection):
        mocked_conn = mock.MagicMock()
        mocked_connection.return_value.__enter__.return_value = mocked_conn
        mocked_conn.execute.side_effect = Exception('Connection Refused')

        results = PostgresCheck.run()
        assert results['REDIS_TO_STREAM'].is_healthy is False
        assert results['REDIS_TO_STREAM'].severity == Result.ERROR

    @mock.patch('checks.redis.RedisToStream.connection')
    def test_bad_connection(self, mocked_connection):
        mocked_connection.return_value.__enter__.return_value = None

        results = PostgresCheck.run()
        assert results['REDIS_TO_STREAM'].is_healthy is False
        assert results['REDIS_TO_STREAM'].severity == Result.WARNING
