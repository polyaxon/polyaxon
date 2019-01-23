# pylint:disable=protected-access
import pytest

from action_manager.actions.webhooks.pagerduty_webhook import (
    PAGER_DUTY_WEBHOOK_ACTION_EXECUTED,
    PagerDutyWebHookAction
)
from action_manager.exceptions import PolyaxonActionException
from tests.test_action_manager.test_webhook_action import TestWebHookAction


@pytest.mark.actions_mark
class TestPagerDutyWebHookAction(TestWebHookAction):
    webhook = PagerDutyWebHookAction

    def test_attrs(self):
        assert self.webhook.action_key == 'pagerduty_webhook'
        assert self.webhook.name == 'PagerDuty WebHook'
        assert self.webhook.event_type == PAGER_DUTY_WEBHOOK_ACTION_EXECUTED

    def test_validate_config(self):
        assert self.webhook._validate_config({
            'url': 'http://pagerduty.com/webhook/foo',
            'method': 'post',
            'service_key': 'foo'
        }) == [{
            'url': 'http://pagerduty.com/webhook/foo',
            'method': 'POST',
            'service_key': 'foo'
        }]

        assert self.webhook._validate_config([{
            'url': 'http://pagerduty.com/webhook/foo',
            'method': 'post',
            'service_key': 'foo'
        }, {
            'url': 'http://pagerduty.com/webhook/bar',
            'method': 'GET'
        }]) == [{
            'url': 'http://pagerduty.com/webhook/foo',
            'method': 'POST',
            'service_key': 'foo'
        }, {
            'url': 'http://pagerduty.com/webhook/bar',
            'method': 'GET',
        }]

    def test_get_config(self):
        assert self.webhook.get_config({
            'url': 'http://foo.com/webhook',
            'method': 'post',
            'service_key': 'foo'
        }) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST',
            'service_key': 'foo'
        }]
        assert self.webhook.get_config([{
            'url': 'http://foo.com/webhook',
            'method': 'post',
            'service_key': 'foo'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET',
            'service_key': 'bar'
        }]) == [{
            'url': 'http://foo.com/webhook',
            'method': 'POST',
            'service_key': 'foo'
        }, {
            'url': 'http://bar.com/webhook',
            'method': 'GET',
            'service_key': 'bar'
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
            'event_type': context.get('event_type'),
            'description': context.get('description'),
            'details': context.get('details'),
            'incident_key': context.get('incident_key'),
            'client': 'Polyaxon',
            'client_url': 'https://polyaxon.com',
            'contexts': context.get('contexts'),
        }

    def test_execute_empty_payload_with_config(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(
                context=None,
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})
