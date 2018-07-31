import pytest

from action_manager.actions.webhooks.slack_webhook import (
    SlackWebHookAction,
    SLACK_WEBHOOK_ACTION_EXECUTED
)
from action_manager.exception import PolyaxonActionException
from tests.test_action_manager.test_webhook_action import TestWebHookAction


@pytest.mark.actions_mark
class TestSlackWebHookAction(TestWebHookAction):
    DISABLE_RUNNER = True
    webhook = SlackWebHookAction

    def test_attrs(self):
        assert self.webhook.action_key == 'slack_webhook'
        assert self.webhook.name == 'Slack WebHook'
        assert self.webhook.event_type == SLACK_WEBHOOK_ACTION_EXECUTED

    def test_validate_config(self):
        assert self.webhook._validate_config({
            'url': 'http://slack.com/webhook/foo',
            'method': 'post',
            'channel': 'foo'
        }) == [{
            'url': 'http://slack.com/webhook/foo',
            'method': 'POST',
            'channel': 'foo'
        }]

        assert self.webhook._validate_config([{
            'url': 'http://slack.com/webhook/foo',
            'method': 'post',
            'channel': 'foo'
        }, {
            'url': 'http://slack.com/webhook/bar',
            'method': 'GET'
        }]) == [{
            'url': 'http://slack.com/webhook/foo',
            'method': 'POST',
            'channel': 'foo'
        }, {
            'url': 'http://slack.com/webhook/bar',
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
            'fallback': context.get('fallback'),
            'title': context.get('title'),
            'title_link': context.get('title_link'),
            'text': context.get('text'),
            'fields': context.get('fields'),
            'mrkdwn_in': ['text'],
            'footer_icon': context.get('footer_icon'),
            'footer': context.get('footer'),
            'color': context.get('color'),
        }

    def test_execute_empty_payload(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(context={})

        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(
                context=None,
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})
