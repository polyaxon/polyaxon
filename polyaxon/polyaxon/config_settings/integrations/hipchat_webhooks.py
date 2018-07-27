import json

from polyaxon.config_manager import config

INTEGRATIONS_HIPCHAT_WEBHOOKS = config.get_string('POLYAXON_INTEGRATIONS_HIPCHAT_WEBHOOKS',
                                                  is_optional=True,
                                                  is_local=True)

if INTEGRATIONS_HIPCHAT_WEBHOOKS:
    # Parse the web hooks
    INTEGRATIONS_HIPCHAT_WEBHOOKS = json.loads(INTEGRATIONS_HIPCHAT_WEBHOOKS)
    if not isinstance(INTEGRATIONS_HIPCHAT_WEBHOOKS, list):
        INTEGRATIONS_HIPCHAT_WEBHOOKS = None
