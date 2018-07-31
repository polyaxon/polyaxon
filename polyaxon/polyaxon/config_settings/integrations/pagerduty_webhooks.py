import json

from polyaxon.config_manager import config

INTEGRATIONS_PAGER_DUTY_WEBHOOKS = config.get_string('POLYAXON_INTEGRATIONS_PAGER_DUTY_WEBHOOKS',
                                                     is_optional=True,
                                                     is_local=True)

if INTEGRATIONS_PAGER_DUTY_WEBHOOKS:
    # Parse the web hooks
    INTEGRATIONS_PAGER_DUTY_WEBHOOKS = json.loads(INTEGRATIONS_PAGER_DUTY_WEBHOOKS)
    if not isinstance(INTEGRATIONS_PAGER_DUTY_WEBHOOKS, list):
        INTEGRATIONS_PAGER_DUTY_WEBHOOKS = None
