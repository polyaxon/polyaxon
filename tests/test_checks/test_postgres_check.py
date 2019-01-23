import mock
import pytest

from checks.postgres import PostgresCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestPostgresHealthCheck(BaseTest):
    def test_database_is_healthy(self):
        results = PostgresCheck.run()
        assert results['POSTGRES'].is_healthy is True

    @mock.patch('checks.postgres.connection.cursor')
    def test_cursor_error(self, mocked_connection):
        mocked_conn = mock.MagicMock()
        mocked_connection.return_value.__enter__.return_value = mocked_conn
        mocked_conn.execute.side_effect = Exception('Connection Refused')

        results = PostgresCheck.run()
        assert results['POSTGRES'].is_healthy is False
        assert results['POSTGRES'].severity == Result.ERROR

    @mock.patch('checks.postgres.connection')
    def test_bad_connection(self, mocked_connection):
        mocked_connection.return_value.__enter__.return_value = None

        results = PostgresCheck.run()
        assert results['POSTGRES'].is_healthy is False
        assert results['POSTGRES'].severity == Result.WARNING
