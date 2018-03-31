from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from factories.pipelines import PipelineFactory, OperationFactory
from tests.utils import BaseTest


class TestOperationModel(BaseTest):
    def setUp(self):
        return super().setUp()

    def test_get_countdown(self):
        operation = OperationFactory(retry_delay=5)
        assert operation.get_countdown(1) == 5
        assert operation.get_countdown(2) == 5

        # Test exponential backoff
        operation.retry_exponential_backoff = True
        operation.max_retry_delay = 24
        operation.save()
        assert operation.get_countdown(1) == 5
        assert operation.get_countdown(2) == 5
        assert operation.get_countdown(3) == 8
        assert operation.get_countdown(4) == 16
        assert operation.get_countdown(5) == 24  # Max retry delay

    def test_get_run_params(self):
        operation = OperationFactory()
        assert operation.get_run_params() == {}

        operation.celery_queue = 'dummy_queue'
        operation.save()
        assert operation.get_run_params() == {'queue': 'dummy_queue'}

        operation.timeout = 10
        operation.save()

        assert operation.get_run_params() == {
            'queue': 'dummy_queue',
            'soft_time_limit': 10,
            'time_limit': settings.CELERY_HARD_TIME_LIMIT_DELAY + 10,
        }

        operation.execute_at = timezone.now() + timedelta(hours=1)
        operation.save()
        assert operation.get_run_params() == {
            'queue': 'dummy_queue',
            'soft_time_limit': 10,
            'time_limit': settings.CELERY_HARD_TIME_LIMIT_DELAY + 10,
            'eta': operation.execute_at
        }
