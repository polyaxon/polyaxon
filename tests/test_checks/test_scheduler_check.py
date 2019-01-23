from unittest.mock import patch

import pytest

from checks.results import Result
from checks.scheduler import SchedulerCheck
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestSchedulerHealthCheck(BaseTest):
    def test_scheduler_is_healthy(self):
        results = SchedulerCheck.run()
        assert results['SCHEDULER'].is_healthy is True

    @patch('scheduler.tasks.health.scheduler_health.apply_async')
    def test_scheduler_wrong_results(self, mock_health):
        mock_health.return_value.__enter__.return_value = None

        results = SchedulerCheck.run()
        assert results['SCHEDULER'].is_healthy is False
        assert results['SCHEDULER'].severity == Result.WARNING

    @patch('scheduler.tasks.health.scheduler_health.apply_async')
    def test_scheduler_not_healthy(self, mock_health):
        mock_health.side_effect = Exception('Connection Refused')

        results = SchedulerCheck.run()
        assert results['SCHEDULER'].is_healthy is False
        assert results['SCHEDULER'].severity == Result.ERROR
