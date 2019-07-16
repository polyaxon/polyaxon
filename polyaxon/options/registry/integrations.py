from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

INTEGRATIONS_WEBHOOKS_DISCORD = '{}{}{}'.format(option_namespaces.INTEGRATIONS_WEBHOOKS,
                                                NAMESPACE_DB_OPTION_MARKER,
                                                option_subjects.DISCORD)
INTEGRATIONS_WEBHOOKS_HIPCHAT = '{}{}{}'.format(option_namespaces.INTEGRATIONS_WEBHOOKS,
                                                NAMESPACE_DB_OPTION_MARKER,
                                                option_subjects.HIPCHAT)
INTEGRATIONS_WEBHOOKS_MATTERMOST = '{}{}{}'.format(option_namespaces.INTEGRATIONS_WEBHOOKS,
                                                   NAMESPACE_DB_OPTION_MARKER,
                                                   option_subjects.MATTERMOST)
INTEGRATIONS_WEBHOOKS_PAGER_DUTY = '{}{}{}'.format(option_namespaces.INTEGRATIONS_WEBHOOKS,
                                                   NAMESPACE_DB_OPTION_MARKER,
                                                   option_subjects.PAGER_DUTY)
INTEGRATIONS_WEBHOOKS_SLACK = '{}{}{}'.format(option_namespaces.INTEGRATIONS_WEBHOOKS,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.SLACK)
INTEGRATIONS_WEBHOOKS_GENERIC = '{}{}{}'.format(option_namespaces.INTEGRATIONS_WEBHOOKS,
                                                NAMESPACE_DB_OPTION_MARKER,
                                                option_subjects.GENERIC)


class IntegrationsWebhooksOption(Option):
    is_global = False
    is_secret = True
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class IntegrationsWebhooksDiscord(IntegrationsWebhooksOption):
    key = INTEGRATIONS_WEBHOOKS_DISCORD
    description = 'Configuration for setting webhooks integration for Discord'


class IntegrationsWebhooksHipchat(IntegrationsWebhooksOption):
    key = INTEGRATIONS_WEBHOOKS_HIPCHAT
    description = 'Configuration for setting webhooks integration for Hipchat'


class IntegrationsWebhooksMattermost(IntegrationsWebhooksOption):
    key = INTEGRATIONS_WEBHOOKS_MATTERMOST
    description = 'Configuration for setting webhooks integration for Mattermost'


class IntegrationsWebhooksPagerDuty(IntegrationsWebhooksOption):
    key = INTEGRATIONS_WEBHOOKS_PAGER_DUTY
    description = 'Configuration for setting webhooks integration for PagerDuty'


class IntegrationsWebhooksSlack(IntegrationsWebhooksOption):
    key = INTEGRATIONS_WEBHOOKS_SLACK
    description = 'Configuration for setting webhooks integration for Slack'


class IntegrationsWebhooksGeneric(IntegrationsWebhooksOption):
    key = INTEGRATIONS_WEBHOOKS_GENERIC
    description = 'Configuration for setting setting a generic webhooks'
