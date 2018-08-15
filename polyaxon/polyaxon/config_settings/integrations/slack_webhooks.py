from polyaxon.config_manager import config

INTEGRATIONS_SLACK_WEBHOOKS = config.get_dict('POLYAXON_INTEGRATIONS_SLACK_WEBHOOKS',
                                              is_list=True,
                                              is_optional=True,
                                              is_local=True)
