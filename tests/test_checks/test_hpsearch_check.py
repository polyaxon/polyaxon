from unittest.mock import patch

import pytest

from checks.hpsearch import HPSearchCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestHPHealthCheck(BaseTest):
    def test_hp_is_healthy(self):
        results = HPSearchCheck.run()
        assert results['HPSEARCH'].is_healthy is True

    @patch('hpsearch.tasks.health.hp_health.apply_async')
    def test_hp_wrong_results(self, mock_health):
        mock_health.return_value.__enter__.return_value = None

        results = HPSearchCheck.run()
        assert results['HPSEARCH'].is_healthy is False
        assert results['HPSEARCH'].severity == Result.WARNING

    @patch('hpsearch.tasks.health.hp_health.apply_async')
    def test_hp_not_healthy(self, mock_health):
        mock_health.side_effect = Exception('Connection Refused')

        results = HPSearchCheck.run()
        assert results['HPSEARCH'].is_healthy is False
        assert results['HPSEARCH'].severity == Result.ERROR
