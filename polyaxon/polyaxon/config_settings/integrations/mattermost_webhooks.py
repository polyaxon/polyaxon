import json

from polyaxon.config_manager import config

INTEGRATIONS_MATTERMOST_WEBHOOKS = config.get_string('POLYAXON_INTEGRATIONS_HIPCHAT_WEBHOOKS',
                                                     is_optional=True,
                                                     is_local=True)

if INTEGRATIONS_MATTERMOST_WEBHOOKS:
    # Parse the web hooks
    INTEGRATIONS_MATTERMOST_WEBHOOKS = json.loads(INTEGRATIONS_MATTERMOST_WEBHOOKS)
    if not isinstance(INTEGRATIONS_MATTERMOST_WEBHOOKS, list):
        INTEGRATIONS_MATTERMOST_WEBHOOKS = None
