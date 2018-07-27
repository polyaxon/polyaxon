import json

from polyaxon.config_manager import config

INTEGRATIONS_WEBHOOKS = config.get_string('POLYAXON_INTEGRATIONS_WEBHOOKS',
                                          is_optional=True,
                                          is_local=True)

if INTEGRATIONS_WEBHOOKS:
    # Parse the web hooks
    INTEGRATIONS_WEBHOOKS = json.loads(INTEGRATIONS_WEBHOOKS)
    if not isinstance(INTEGRATIONS_WEBHOOKS, list):
        INTEGRATIONS_WEBHOOKS = None
