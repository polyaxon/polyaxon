# pylint:disable=protected-access
from unittest.mock import patch

import pytest

from action_manager.actions.webhooks.webhook import WEBHOOK_ACTION_EXECUTED, WebHookAction
from action_manager.exceptions import PolyaxonActionException
from tests.utils import BaseTest


@pytest.mark.actions_mark
class TestWebHookAction(BaseTest):
    webhook = WebHookAction

    def test_attrs(self):
        assert self.webhook.action_key == 'webhook'
        assert self.webhook.name == 'WebHook'
        assert self.webhook.event_type == WEBHOOK_ACTION_EXECUTED

    def test_validate_empty_config(self):
        assert self.webhook._validate_config({}) == []
        assert self.webhook._validate_config([]) == []
        assert self.webhook._validate_config({'foo': 'bar'}) == []

    def test_validate_config_raises_for_wrong_configs(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook._validate_config({'url': 'bar'})

        with self.assertRaises(PolyaxonActionException):
            self.webhook._validate_config({'url': 'http://foo.com/webhook', 'method': 1})

        with self.assertRaises(PolyaxonActionException):
            self.webhook._validate_config({'url': 'http://foo.com/webhook', 'method': 'foo'})

    def test_validate_config(self):
        assert self.webhook._validate_config({
            'url': 'http://foo.com/webhook',
            'method': 'post'
        }) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST'
        }]

        assert self.webhook._validate_config([{
            'url': 'http://foo.com/webhook',
            'method': 'post'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET'
        }]) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET'
        }]

    def test_get_empty_config(self):
        assert self.webhook.get_config() == []
        assert self.webhook.get_config({}) == []
        assert self.webhook.get_config({'foo': 'bar'}) == []

    def test_get_config(self):
        assert self.webhook.get_config({
            'url': 'http://foo.com/webhook',
            'method': 'post'
        }) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST'
        }]
        assert self.webhook.get_config([{
            'url': 'http://foo.com/webhook',
            'method': 'post'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET'
        }]) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET'
        }]

    def test_prepare(self):
        assert self.webhook._prepare(None) is None
        assert self.webhook._prepare({}) == {}
        assert self.webhook._prepare({'foo': 'bar'}) == {'foo': 'bar'}

    def test_execute_empty_payload(self):
        with patch('action_manager.actions.webhooks.webhook.safe_request') as mock_execute:
            self.webhook.execute(context={})

        assert mock_execute.call_count == 0

    def test_execute_empty_payload_with_config(self):
        with patch('action_manager.actions.webhooks.webhook.safe_request') as mock_execute:
            self.webhook.execute(
                context=None,
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})

        assert mock_execute.call_count == 1

    def test_execute(self):
        with patch('action_manager.actions.webhooks.webhook.safe_request') as mock_execute:
            self.webhook.execute(context={'foo': 'bar'})

        assert mock_execute.call_count == 0

        with patch('action_manager.actions.webhooks.webhook.safe_request') as mock_execute:
            self.webhook.execute(
                context={'foo': 'bar'},
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})

        assert mock_execute.call_count == 1
