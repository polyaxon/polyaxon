from django.conf import settings

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from action_manager.exception import PolyaxonActionException
from event_manager.event_actions import EXECUTED

DISCORD_WEBHOOK_ACTION_EXECUTED = 'discord_webhook_action.{}'.format(EXECUTED)


class DiscordWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = DISCORD_WEBHOOK_ACTION_EXECUTED


class DiscordWebHookAction(WebHookAction):
    action_key = 'discord_webhook'
    name = 'Discord WebHook'
    event_type = DISCORD_WEBHOOK_ACTION_EXECUTED
    description = "Discord webhooks to send payload to a discord room."
    raise_empty_context = True

    @classmethod
    def _get_config(cls):
        """Configuration for discord webhooks.

        should be a list of urls and potentially a method.

        If no method is given, then by default we use POST.
        """
        return settings.INTEGRATIONS_DISCORD_WEBHOOKS

    @classmethod
    def _prepare(cls, context):
        context = super()._prepare(context)

        payload = {
            'username': 'Polyaxon',
            'avatar_url': context.get('avatar_url'),
            'tts': context.get('tts', False)
        }
        content = context.get('content')
        if content and len(content) <= 2000:
            payload['content'] = content
        else:
            raise PolyaxonActionException(
                'Discord content must non null and 2000 or fewer characters.')

        proxy = context.get('proxy')
        if proxy:
            payload['https'] = proxy
        return payload
