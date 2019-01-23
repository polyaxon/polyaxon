from unittest.mock import patch

import pytest

from checks.logs import LogsCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestLogsHealthCheck(BaseTest):
    def test_logs_is_healthy(self):
        results = LogsCheck.run()
        assert results['LOGS'].is_healthy is True

    @patch('logs_handlers.tasks.health.logs_health.apply_async')
    def test_logs_wrong_results(self, mock_health):
        mock_health.return_value.__enter__.return_value = None

        results = LogsCheck.run()
        assert results['LOGS'].is_healthy is False
        assert results['LOGS'].severity == Result.WARNING

    @patch('logs_handlers.tasks.health.logs_health.apply_async')
    def test_logs_not_healthy(self, mock_health):
        mock_health.side_effect = Exception('Connection Refused')

        results = LogsCheck.run()
        assert results['LOGS'].is_healthy is False
        assert results['LOGS'].severity == Result.ERROR
