# pylint:disable=protected-access
from unittest.mock import patch

import pytest

from action_manager.actions.webhooks.discord_webhook import (
    DISCORD_WEBHOOK_ACTION_EXECUTED,
    DiscordWebHookAction
)
from action_manager.exceptions import PolyaxonActionException
from tests.test_action_manager.test_webhook_action import TestWebHookAction


@pytest.mark.actions_mark
class TestDiscordWebHookAction(TestWebHookAction):
    webhook = DiscordWebHookAction

    def test_attrs(self):
        assert self.webhook.action_key == 'discord_webhook'
        assert self.webhook.name == 'Discord WebHook'
        assert self.webhook.event_type == DISCORD_WEBHOOK_ACTION_EXECUTED

    def test_prepare(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook._prepare(None)
        with self.assertRaises(PolyaxonActionException):
            self.webhook._prepare({})

        context = {
            'content': 'message',
        }
        assert self.webhook._prepare(context) == {
            'username': 'Polyaxon',
            'avatar_url': context.get('avatar_url'),
            'tts': context.get('tts', False),
            'content': 'message'
        }

    def test_execute_empty_payload_with_config(self):
        with self.assertRaises(PolyaxonActionException):
            self.webhook.execute(
                context=None,
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})

    def test_execute(self):
        with patch('action_manager.actions.webhooks.webhook.safe_request') as mock_execute:
            self.webhook.execute(context={'content': 'bar'})

        assert mock_execute.call_count == 0

        with patch('action_manager.actions.webhooks.webhook.safe_request') as mock_execute:
            self.webhook.execute(
                context={'content': 'bar'},
                config={'url': 'http://bar.com/webhook', 'method': 'GET'})

        assert mock_execute.call_count == 1
