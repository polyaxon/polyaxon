# pylint:disable=protected-access
import pytest

from action_manager.actions.webhooks.mattermost_webhook import (
    MATTERMOST_WEBHOOK_ACTION_EXECUTED,
    MattermostWebHookAction
)
from action_manager.exceptions import PolyaxonActionException
from tests.test_action_manager.test_webhook_action import TestWebHookAction


@pytest.mark.actions_mark
class TestMattermostWebHookAction(TestWebHookAction):
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
            'attachments': [{
                'pretext': context.get('pretext'),
                'title': context.get('title'),
                'text': context.get('text'),
                'color': context.get('color'),
                'fields': None,
                'author_name': 'Polyaxon',
                'author_link': 'https://polyaxon.com',
                'author_icon': None
            }]
        }

    def test_execute_empty_payload_with_config(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(
                context=None,
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})
