from typing import Dict, List

import conf

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from action_manager.utils import pagerduty
from event_manager.event import Event
from event_manager.event_actions import EXECUTED

PAGER_DUTY_WEBHOOK_ACTION_EXECUTED = 'pagerduty_webhook_action.{}'.format(EXECUTED)


class PagerDutyWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = PAGER_DUTY_WEBHOOK_ACTION_EXECUTED


class PagerDutyWebHookAction(WebHookAction):
    action_key = 'pagerduty_webhook'
    name = 'PagerDuty WebHook'
    event_type = PAGER_DUTY_WEBHOOK_ACTION_EXECUTED
    description = "PagerDuty webhooks to send event payload to pagerduty."
    raise_empty_context = True

    @classmethod
    def _validate_config(cls, config: Dict) -> List[Dict]:
        if not config:
            return []
        return cls._get_valid_config(config, 'service_key')

    @classmethod
    def _get_config(cls) -> Dict:
        """Configuration for pagerduty webhooks.

        should be a list of urls and potentially a method and service key.

        If no method is given, then by default we use POST.
        """
        return conf.get('INTEGRATIONS_PAGER_DUTY_WEBHOOKS')

    @classmethod
    def serialize_event_to_context(cls, event: Event) -> Dict:
        return pagerduty.serialize_event_to_context(event)

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        return {
            'event_type': context.get('event_type'),
            'description': context.get('description'),
            'details': context.get('details'),
            'incident_key': context.get('incident_key'),
            'client': context.get('client', 'Polyaxon'),
            'client_url': context.get('client_url', 'https://polyaxon.com'),
            'contexts': context.get('contexts'),
        }

    @classmethod
    def _pre_execute_web_hook(cls, data: Dict, config: Dict) -> Dict:
        service_key = config.get('service_key')
        if service_key:
            data['service_key'] = service_key

        return data
