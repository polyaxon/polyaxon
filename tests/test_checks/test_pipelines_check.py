from unittest.mock import patch

import pytest

from checks.pipelines import PipelinesCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestPipelinesHealthCheck(BaseTest):
    def test_hp_is_healthy(self):
        results = PipelinesCheck.run()
        assert results['PIPELINES'].is_healthy is True

    @patch('pipelines.health.pipelines_health.apply_async')
    def test_pipelines_wrong_results(self, mock_health):
        mock_health.return_value.__enter__.return_value = None

        results = PipelinesCheck.run()
        assert results['PIPELINES'].is_healthy is False
        assert results['PIPELINES'].severity == Result.WARNING

    @patch('pipelines.health.pipelines_health.apply_async')
    def test_pipelines_not_healthy(self, mock_health):
        mock_health.side_effect = Exception('Connection Refused')

        results = PipelinesCheck.run()
        assert results['PIPELINES'].is_healthy is False
        assert results['PIPELINES'].severity == Result.ERROR
