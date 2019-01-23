import mock
import pytest

from amqp.exceptions import AccessRefused

from django.test import override_settings

from checks.rabbitmq import RabbitMQCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestRabbitMQHealthCheck(BaseTest):
    @override_settings(CELERY_BROKER_URL='broker_url')
    @mock.patch('checks.rabbitmq.Connection')
    def test_broker_refused_connection(self, mocked_connection):
        mocked_conn = mock.MagicMock()
        mocked_connection.return_value.__enter__.return_value = mocked_conn
        mocked_conn.connect.side_effect = ConnectionRefusedError('Connection Refused')

        results = RabbitMQCheck.run()
        assert results['RABBITMQ'].is_healthy is False
        assert results['RABBITMQ'].severity == Result.ERROR
        mocked_connection.assert_called_once_with('broker_url')

    @override_settings(CELERY_BROKER_URL='broker_url')
    @mock.patch('checks.rabbitmq.Connection')
    def test_broker_access_refused(self, mocked_connection):
        mocked_conn = mock.MagicMock()
        mocked_connection.return_value.__enter__.return_value = mocked_conn
        mocked_conn.connect.side_effect = AccessRefused('Access Refused')

        results = RabbitMQCheck.run()
        assert results['RABBITMQ'].is_healthy is False
        assert results['RABBITMQ'].severity == Result.ERROR
        mocked_connection.assert_called_once_with('broker_url')

    @override_settings(CELERY_BROKER_URL=None)
    @mock.patch('checks.rabbitmq.Connection')
    def test_broker_connection_upon_none_url(self, mocked_connection):
        mocked_conn = mock.MagicMock()
        mocked_connection.return_value.__enter__.return_value = mocked_conn
        mocked_conn.connect.side_effect = AccessRefused('Connection Refused')

        results = RabbitMQCheck.run()
        assert results['RABBITMQ'].is_healthy is False
        assert results['RABBITMQ'].severity == Result.ERROR
        mocked_connection.assert_called_once_with(None)
