import json

from polyaxon.config_manager import config

INTEGRATIONS_SLACK_WEBHOOKS = config.get_string('POLYAXON_INTEGRATIONS_SLACK_WEBHOOKS',
                                                is_optional=True,
                                                is_local=True)

if INTEGRATIONS_SLACK_WEBHOOKS:
    # Parse the web hooks
    INTEGRATIONS_SLACK_WEBHOOKS = json.loads(INTEGRATIONS_SLACK_WEBHOOKS)
    if not isinstance(INTEGRATIONS_SLACK_WEBHOOKS, list):
        INTEGRATIONS_SLACK_WEBHOOKS = None
