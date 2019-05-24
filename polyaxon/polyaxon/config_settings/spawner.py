from polyaxon.config_manager import config

PUBLIC_PLUGIN_JOBS = config.get_boolean('POLYAXON_PUBLIC_PLUGIN_JOBS', is_optional=True)

# k8s
K8S_SERVICE_ACCOUNT_NAME = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_NAME')
K8S_SERVICE_ACCOUNT_EXPERIMENTS = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_EXPERIMENTS',
                                                    is_optional=True)
K8S_SERVICE_ACCOUNT_JOBS = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_JOBS',
                                             is_optional=True)
K8S_SERVICE_ACCOUNT_BUILDS = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_BUILDS',
                                               is_optional=True)
K8S_RBAC_ENABLED = config.get_boolean('POLYAXON_K8S_RBAC_ENABLED')
K8S_INGRESS_ENABLED = config.get_boolean('POLYAXON_K8S_INGRESS_ENABLED')
K8S_INGRESS_ANNOTATIONS = config.get_string('POLYAXON_K8S_INGRESS_ANNOTATIONS', is_optional=True)

# Refs
REFS_SECRETS = config.get_string('POLYAXON_REFS_SECRETS',
                                 is_optional=True,
                                 is_list=True,
                                 default=())
REFS_CONFIG_MAPS = config.get_string('POLYAXON_REFS_CONFIG_MAPS',
                                     is_optional=True,
                                     is_list=True,
                                     default=())


# DNS Cluster
DNS_USE_RESOLVER = config.get_boolean('POLYAXON_DNS_USE_RESOLVER',
                                      is_optional=True,
                                      default=False)
DNS_CUSTOM_CLUSTER = config.get_string('POLYAXON_DNS_CUSTOM_CLUSTER',
                                       is_optional=True,
                                       default='cluster.local')

# Roles
ROLE_LABELS_WORKER = config.get_string('POLYAXON_ROLE_LABELS_WORKER')
ROLE_LABELS_DASHBOARD = config.get_string('POLYAXON_ROLE_LABELS_DASHBOARD')
ROLE_LABELS_LOG = config.get_string('POLYAXON_ROLE_LABELS_LOG')
ROLE_LABELS_API = config.get_string('POLYAXON_ROLE_LABELS_API')
ROLE_LABELS_CONFIG = config.get_string('POLYAXON_ROLE_LABELS_CONFIG')
ROLE_LABELS_HOOKS = config.get_string('POLYAXON_ROLE_LABELS_HOOKS')

# Types
TYPE_LABELS_CORE = config.get_string('POLYAXON_TYPE_LABELS_CORE')
TYPE_LABELS_RUNNER = config.get_string('POLYAXON_TYPE_LABELS_RUNNER')

# SECURITY CONTEXT
SECURITY_CONTEXT_USER = config.get_int('POLYAXON_SECURITY_CONTEXT_USER',
                                       is_optional=True)
SECURITY_CONTEXT_GROUP = config.get_int('POLYAXON_SECURITY_CONTEXT_GROUP',
                                        is_optional=True)
# Plugins
PLUGINS = config.get_dict_of_dicts('POLYAXON_PLUGINS',
                                   is_optional=True,
                                   default={})
