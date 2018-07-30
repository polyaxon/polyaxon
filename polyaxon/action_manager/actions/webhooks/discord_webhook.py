from django.conf import settings

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from action_manager.exception import PolyaxonActionException
from event_manager.event_actions import EXECUTED

DISCORD_WEBHOOK_ACTION_EXECUTED = 'discord_webhook_action.{}'.format(EXECUTED)


class DiscordWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = DISCORD_WEBHOOK_ACTION_EXECUTED


class DiscordWebHookAction(WebHookAction):
    key = 'discord_webhook'
    name = 'Discord WebHook'
    event_type = DISCORD_WEBHOOK_ACTION_EXECUTED
    description = "Discord webhooks to send payload to a discord room."

    def _get_config(self):
        """Configuration for discord webhooks.

        should be a list of urls and potentially a method.

        If no method is given, then by default we use POST.
        """
        return self._get_from_settings(settings.INTEGRATIONS_DISCORD_WEBHOOKS)

    def _prepare(self, context):
        payload = {
            'username': 'Polyaxon',
            'avatar_url': context.get('avatar_url'),
            'tts': context.get('tts', False)
        }
        message = context.get('message')
        if message and len(message) <= 2000:
            payload['content'] = message
        else:
            raise PolyaxonActionException(
                'Discord message must non null and 2000 or fewer characters.')

        proxy = context.get('proxy')
        if proxy:
            payload['https'] = proxy
        return payload
