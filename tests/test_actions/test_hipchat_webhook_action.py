# pylint:disable=protected-access
import pytest

from actions.exceptions import PolyaxonActionException
from actions.registry.webhooks.hipchat_webhook import (
    HIPCHAT_WEBHOOK_ACTION_EXECUTED,
    HipChatWebHookAction
)
from tests.test_actions.test_webhook_action import TestWebHookAction


@pytest.mark.actions_mark
class TestHipChatWebHookAction(TestWebHookAction):
    webhook = HipChatWebHookAction

    def test_attrs(self):
        assert self.webhook.action_key == 'hipchat_webhook'
        assert self.webhook.name == 'HipChat WebHook'
        assert self.webhook.event_type == HIPCHAT_WEBHOOK_ACTION_EXECUTED

    def test_prepare(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook._prepare(None)
        with self.assertRaises(PolyaxonActionException):
            self.webhook._prepare({})

        context = {
            'message': 'message',
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

    def test_execute_empty_payload_with_config(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(
                context=None,
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})
