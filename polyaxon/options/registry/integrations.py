from options import option_namespaces, option_subjects
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


class IntegrationsWebhooksDiscord(Option):
    key = INTEGRATIONS_WEBHOOKS_DISCORD
    is_global = False
    is_secret = True
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Configuration for setting webhooks integration for Discord'


class IntegrationsWebhooksHipchat(Option):
    key = INTEGRATIONS_WEBHOOKS_HIPCHAT
    is_global = False
    is_secret = True
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Configuration for setting webhooks integration for Hipchat'


class IntegrationsWebhooksMattermost(Option):
    key = INTEGRATIONS_WEBHOOKS_MATTERMOST
    is_global = False
    is_secret = True
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Configuration for setting webhooks integration for Mattermost'


class IntegrationsWebhooksPagerDuty(Option):
    key = INTEGRATIONS_WEBHOOKS_PAGER_DUTY
    is_global = False
    is_secret = True
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Configuration for setting webhooks integration for PagerDuty'


class IntegrationsWebhooksSlack(Option):
    key = INTEGRATIONS_WEBHOOKS_SLACK
    is_global = False
    is_secret = True
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Configuration for setting webhooks integration for Slack'


class IntegrationsWebhooksGeneric(Option):
    key = INTEGRATIONS_WEBHOOKS_GENERIC
    is_global = False
    is_secret = True
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Configuration for setting setting a generic webhooks'
