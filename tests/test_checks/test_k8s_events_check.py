from unittest.mock import patch

import pytest

from checks.k8s_events import K8SEventsCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestK8SEventsHealthCheck(BaseTest):
    def test_k8s_events_is_healthy(self):
        results = K8SEventsCheck.run()
        assert results['K8SEVENTS'].is_healthy is True

    @patch('k8s_events_handlers.tasks.health.k8s_events_health.apply_async')
    def test_k8s_events_wrong_results(self, mock_health):
        mock_health.return_value.__enter__.return_value = None

        results = K8SEventsCheck.run()
        assert results['K8SEVENTS'].is_healthy is False
        assert results['K8SEVENTS'].severity == Result.WARNING

    @patch('k8s_events_handlers.tasks.health.k8s_events_health.apply_async')
    def test_k8s_events_not_healthy(self, mock_health):
        mock_health.side_effect = Exception('Connection Refused')

        results = K8SEventsCheck.run()
        assert results['K8SEVENTS'].is_healthy is False
        assert results['K8SEVENTS'].severity == Result.ERROR
