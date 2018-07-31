import json

from polyaxon.config_manager import config

INTEGRATIONS_DISCORD_WEBHOOKS = config.get_string('POLYAXON_INTEGRATIONS_DISCORD_WEBHOOKS',
                                                  is_optional=True,
                                                  is_local=True)

if INTEGRATIONS_DISCORD_WEBHOOKS:
    # Parse the web hooks
    INTEGRATIONS_DISCORD_WEBHOOKS = json.loads(INTEGRATIONS_DISCORD_WEBHOOKS)
    if not isinstance(INTEGRATIONS_DISCORD_WEBHOOKS, list):
        INTEGRATIONS_DISCORD_WEBHOOKS = None
