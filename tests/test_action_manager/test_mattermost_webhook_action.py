import pytest

from action_manager.actions.webhooks.mattermost_webhook import (
    MattermostWebHookAction,
    MATTERMOST_WEBHOOK_ACTION_EXECUTED
)
from action_manager.exception import PolyaxonActionException
from tests.test_action_manager.test_webhook_action import TestWebHookAction


@pytest.mark.actions_mark
class TestMattermostWebHookAction(TestWebHookAction):
    DISABLE_RUNNER = True
    webhook = MattermostWebHookAction

    def test_attrs(self):
        assert self.webhook.action_key == 'mattermost_webhook'
        assert self.webhook.name == 'Mattermost WebHook'
        assert self.webhook.event_type == MATTERMOST_WEBHOOK_ACTION_EXECUTED

    def test_validate_config(self):
        assert self.webhook._validate_config({
            'url': 'http://mattermost.com/webhook/foo',
            'method': 'post',
            'channel': 'foo'
        }) == [{
            'url': 'http://mattermost.com/webhook/foo',
            'method': 'POST',
            'channel': 'foo'
        }]

        assert self.webhook._validate_config([{
            'url': 'http://mattermost.com/webhook/foo',
            'method': 'post',
            'channel': 'foo'
        }, {
            'url': 'http://mattermost.com/webhook/bar',
            'method': 'GET'
        }]) == [{
            'url': 'http://mattermost.com/webhook/foo',
            'method': 'POST',
            'channel': 'foo'
        }, {
            'url': 'http://mattermost.com/webhook/bar',
            'method': 'GET',
            'channel': None
        }]

    def test_get_config(self):
        assert self.webhook.get_config({
            'url': 'http://foo.com/webhook',
            'method': 'post',
            'channel': 'foo'
        }) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST',
            'channel': 'foo'
        }]
        assert self.webhook.get_config([{
            'url': 'http://foo.com/webhook',
            'method': 'post',
            'channel': 'foo'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET',
            'channel': 'bar'
        }]) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST',
            'channel': 'foo'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET',
            'channel': 'bar'
        }]

    def test_prepare(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook._prepare(None)
        with self.assertRaises(PolyaxonActionException):
            self.webhook._prepare({})

        context = {
            'title': 'title',
            'text': 'text'
        }
        assert self.webhook._prepare(context) == {
            'message': context.get('message'),
            'message_format': context.get('message_format', 'html'),
            'color': context.get('color'),
            'from': 'Polyaxon',
            'attach_to': context.get('attach_to'),
            'notify': context.get('notify', False),
            'card': context.get('card')
        }

    def test_execute_empty_payload(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(context={})

        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(
                context=None,
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})
