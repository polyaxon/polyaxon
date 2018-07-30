from django.conf import settings

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from event_manager.event_actions import EXECUTED

PAGER_DUTY_WEBHOOK_ACTION_EXECUTED = 'pagerduty_webhook_action.{}'.format(EXECUTED)


class PagerDutyWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = PAGER_DUTY_WEBHOOK_ACTION_EXECUTED


class PagerDutyWebHookAction(WebHookAction):
    action_key = 'pagerduty_webhook'
    name = 'PagerDuty WebHook'
    event_type = PAGER_DUTY_WEBHOOK_ACTION_EXECUTED
    description = "PagerDuty webhooks to send event payload to pagerduty."

    def _get_config(self):
        """Configuration for pagerduty webhooks.

        should be a list of urls and potentially a method and service key.

        If no method is given, then by default we use POST.
        """
        return self._get_from_settings(settings.INTEGRATIONS_PAGER_DUTY_WEBHOOKS, 'service_key')

    def _prepare(self, context):
        return {
            'event_type': context.get('event_type'),
            'description': context.get('description'),
            'details': context.get('details'),
            'incident_key': context.get('incident_key'),
            'client': 'polyaxon',
            # 'client_url': get_absolute_uri(),
            'contexts': context.get('contexts'),
        }

    def _pre_execute_web_hook(self, data, config):
        service_key = config.get('service_key')
        if service_key:
            data['service_key'] = service_key

        return data
