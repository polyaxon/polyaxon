from django.conf import settings

from action_manager.action import Action, logger
from action_manager.action_event import ActionExecutedEvent
from event_manager.event_actions import EXECUTED
from libs.http import safe_urlopen

WEBHOOK_ACTION_EXECUTED = 'webhook_action.{}'.format(EXECUTED)


class WebHookActionExecutedEvent(ActionExecutedEvent):
    event_type = WEBHOOK_ACTION_EXECUTED


class WebHookAction(Action):
    key = 'webhook'
    name = 'WebHook'
    event_type = WEBHOOK_ACTION_EXECUTED
    description = ("Webhooks send an HTTP payload to the webhook's configured URL."
                   "Webhooks can be used automaticaly "
                   "by subscribing to certain events on Polyaxon, "
                   "or manually triggered by a user operation.")

    def _get_from_settings(self, settings_env_var, *fields):
        web_hooks = []
        for web_hook in settings_env_var:
            if not web_hook.get('url'):
                logger.warning("Settings contains a non compatible web hook: `%s`", web_hook)
                continue

            method = web_hook.get('method', 'POST')
            if not isinstance(method, str):
                logger.warning("Settings contains a non compatible web hook method: `%s`", method)
                continue

            _method = method.upper()
            if _method not in ['GET', 'POST']:
                logger.warning("Settings contains a non compatible web hook method: `%s`", _method)
                continue

            result_web_hook = {'url': web_hook['url'], 'method': _method}
            for field in fields:
                result_web_hook[field] = web_hook.get(field)
            web_hooks.append(result_web_hook)

        return web_hooks

    def _get_config(self):
        """Configuration for webhooks.

        Should be a list of urls and potentially a method.

        If no method is given, then by default we use POST.
        """
        return self._get_from_settings(settings.INTEGRATIONS_WEBHOOKS)

    def _pre_execute_web_hook(self, data, config):
        return data

    def _execute(self, data, config):
        for web_hook in config:
            data = self._pre_execute_web_hook(data=data, config=config)
            if web_hook['method'] == 'POST':
                safe_urlopen(url=web_hook['url'], method=web_hook['method'], json=data)
            else:
                safe_urlopen(url=web_hook['url'], method=web_hook['method'], params=data)
