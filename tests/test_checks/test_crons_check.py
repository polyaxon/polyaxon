from unittest.mock import patch

import pytest

from checks.crons import CronsCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestCronsHealthCheck(BaseTest):
    def test_crons_is_healthy(self):
        results = CronsCheck.run()
        assert results['CRONS'].is_healthy is True

    @patch('crons.tasks.health.crons_health.apply_async')
    def test_crons_wrong_results(self, mock_health):
        mock_health.return_value.__enter__.return_value = None

        results = CronsCheck.run()
        assert results['CRONS'].is_healthy is False
        assert results['CRONS'].severity == Result.WARNING

    @patch('crons.tasks.health.crons_health.apply_async')
    def test_crons_not_healthy(self, mock_health):
        mock_health.side_effect = Exception('Connection Refused')

        results = CronsCheck.run()
        assert results['CRONS'].is_healthy is False
        assert results['CRONS'].severity == Result.ERROR
