from django.conf import settings

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from event_manager.event_actions import EXECUTED

MATTERMOST_WEBHOOK_ACTION_EXECUTED = 'mattermost_webhook_action.{}'.format(EXECUTED)


class MattermostWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = MATTERMOST_WEBHOOK_ACTION_EXECUTED


class MattermostWebHookAction(WebHookAction):
    key = 'mattermost_webhook'
    name = 'Mattermost WebHook'
    event_type = MATTERMOST_WEBHOOK_ACTION_EXECUTED
    description = "Mattermost webhooks to send payload to a Mattermost channel."

    def _get_config(self):
        """Configuration for mattermost webhooks.

        should be a list of urls and potentially a method.

        If no method is given, then by default we use POST.
        """
        return self._get_from_settings(settings.INTEGRATIONS_MATTERMOST_WEBHOOKS, 'channel')

    def _prepare(self, context):
        return {
            'message': context.get('message'),
            'message_format': context.get('message_format', 'html'),
            'color': context.get('color'),
            'from': 'Polyaxon',
            'attach_to': context.get('attach_to'),
            'notify': context.get('notify', False),
            'card': context.get('card')
        }

    def _pre_execute_web_hook(self, data, config):
        channel = config.get('channel')
        if channel:
            data['channel'] = channel

        return data
