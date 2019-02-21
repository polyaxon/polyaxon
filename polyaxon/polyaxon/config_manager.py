import base64
import os
import uuid

from distutils.util import strtobool  # pylint:disable=import-error

import rhea

from unipath import Path

from django.utils.functional import cached_property


def base_directory():
    return Path(__file__).ancestor(3)


ROOT_DIR = base_directory()
DATA_DIR = ROOT_DIR.child('data')
ENV_VARS_DIR = ROOT_DIR.child('polyaxon').child('polyaxon').child('env_vars')
TESTING = bool(strtobool(os.getenv('TESTING', "0")))


class ConfigManager(rhea.Rhea):
    _PASS = '-Z$Swjin_bdNPtaV4nQEn&gWb;T|'

    @cached_property
    def decode_iterations(self):
        return self.get_int('_POLYAXON_DECODE_ITERATION', is_optional=True, default=1)

    def _decode(self, value, iteration=3):
        iteration = iteration or self.decode_iterations

        def _decode_once():
            return base64.b64decode(value).decode('utf-8')

        for _ in range(iteration):
            value = _decode_once()
        return value

    @staticmethod
    def _encode(value):
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')

    def __init__(self, **params):
        super().__init__(**params)
        self._env = self.get_string('POLYAXON_ENVIRONMENT')
        self._service = self.get_string('POLYAXON_SERVICE', is_local=True)
        self._is_debug_mode = self.get_boolean('POLYAXON_DEBUG', is_optional=True, default=False)
        self._namespace = self.get_string('POLYAXON_K8S_NAMESPACE')
        self._cluster_id = self.get_string('POLYAXON_CLUSTER_ID',
                                           is_optional=True,
                                           default=uuid.uuid4())
        self._log_level = self.get_string('POLYAXON_LOG_LEVEL',
                                          is_local=True,
                                          is_optional=True,
                                          default='WARNING').upper()
        self._enable_scheduler = self.get_boolean('POLYAXON_ENABLE_SCHEDULER',
                                                  is_optional=True,
                                                  default=True)
        self._enable_notifier = self.get_boolean('POLYAXON_ENABLE_NOTIFIER',
                                                 is_optional=True,
                                                 default=True)
        self._enable_activitylogs = self.get_boolean('POLYAXON_ENABLE_ACTIVITY_LOGS',
                                                     is_optional=True,
                                                     default=True)
        self._chart_version = self.get_string('POLYAXON_CHART_VERSION',
                                              is_optional=True,
                                              default='0.0.0')
        if self.is_sidecar_service or self.is_dockerizer_service:
            self._node_name = None
        else:
            self._node_name = self.get_string('POLYAXON_K8S_NODE_NAME', is_local=True)

    @property
    def namespace(self):
        return self._namespace

    @property
    def cluster_id(self):
        return self._cluster_id

    @property
    def chart_version(self):
        return self._chart_version

    @property
    def node_name(self):
        return self._node_name

    @property
    def service(self):
        return self._service

    @property
    def is_monolith_service(self):
        return self.service == 'monolith'

    @property
    def is_api_service(self):
        return self.service == 'api'

    @property
    def is_commands_service(self):
        return self.service == 'commands'

    @property
    def is_dockerizer_service(self):
        return self.service == 'dockerizer'

    @property
    def is_crons_service(self):
        return self.service == 'crons'

    @property
    def is_monitor_namespace_service(self):
        return self.service == 'monitor_namespace'

    @property
    def is_monitor_resources_service(self):
        return self.service == 'monitor_resources'

    @property
    def is_scheduler_service(self):
        return self.service == 'scheduler'

    @property
    def is_monitor_statuses_service(self):
        return self.service == 'monitor_statuses'

    @property
    def is_sidecar_service(self):
        return self.service == 'sidecar'

    @property
    def is_streams_service(self):
        return self.service == 'streams'

    @property
    def is_hpsearch_service(self):
        return self.service == 'hpsearch'

    @property
    def is_events_handlers_service(self):
        return self.service == 'events_handlers'

    @property
    def is_k8s_events_handlers_service(self):
        return self.service == 'k8s_events_handlers'

    @property
    def is_logs_handlers_service(self):
        return self.service == 'logs_handlers'

    @property
    def is_debug_mode(self):
        return self._is_debug_mode

    @property
    def env(self):
        return self._env

    @property
    def is_testing_env(self):
        if TESTING:
            return True
        if self.env == 'testing':
            return True
        return False

    @property
    def is_local_env(self):
        if self.env == 'local':
            return True
        return False

    @property
    def is_staging_env(self):
        if self.env == 'staging':
            return True
        return False

    @property
    def is_production_env(self):
        if self.env == 'production':
            return True
        return False

    @property
    def log_handlers(self):
        return ['console', 'sentry']

    @property
    def log_level(self):
        if config.is_staging_env:
            return self._log_level
        elif self._log_level == 'DEBUG':
            return 'INFO'
        return self._log_level

    def setup_auditor_services(self):
        if not self.is_testing_env:
            import activitylogs
            import auditor
            import executor
            import notifier
            import tracker

            auditor.validate()
            auditor.setup()
            tracker.validate()
            tracker.setup()
            if self._enable_activitylogs:
                activitylogs.validate()
                activitylogs.setup()
            if self._enable_notifier:
                notifier.validate()
                notifier.setup()
            if self._enable_scheduler:
                executor.validate()
                executor.setup()

    def setup_conf_service(self):
        import conf

        conf.validate()
        conf.setup()

    def setup_ci_service(self):
        import ci

        ci.validate()
        ci.setup()

    def setup_publisher_service(self):
        import publisher

        publisher.validate()
        publisher.setup()

    def setup_query_service(self):
        import query

        query.validate()
        query.setup()

    def setup_ownership_service(self):
        import ownership

        ownership.validate()
        ownership.setup()

    def setup_access_service(self):
        import access

        access.validate()
        access.setup()

    def setup_admin_service(self):
        import administration

        administration.validate()
        administration.setup()

    def setup_stats_service(self):
        import stats

        stats.validate()
        stats.setup()

    def setup_stores_service(self):
        import stores

        stores.validate()
        stores.setup()

    @cached_property
    def notification_url(self):
        value = self.get_string(
            '_POLYAXON_NOTIFICATION',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value) if value else None

    @cached_property
    def ignore_exceptions(self):
        return self.get_string(
            '_POLYAXON_IGNORE_EXCEPTIONS',
            is_list=True,
            is_secret=True,
            is_local=True,
            is_optional=True,
            default=[])

    @cached_property
    def platform_dsn(self):
        value = self.get_string(
            '_POLYAXON_PLATFORM_DSN',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value) if value else None

    @cached_property
    def cli_dsn(self):
        value = self.get_string(
            '_POLYAXON_CLI_DSN',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value, 2) if value else None

    @cached_property
    def tracker_key(self):
        value = self.get_string(
            '_POLYAXON_TRACKER_KEY',
            is_secret=True,
            is_local=True,
            is_optional=True)
        return self._decode(value) if value else None


config_values = [
    '{}/defaults.json'.format(ENV_VARS_DIR),
    os.environ,
]

if TESTING:
    config_values.append('{}/test.json'.format(ENV_VARS_DIR))
elif os.path.isfile('{}/local.json'.format(ENV_VARS_DIR)):
    config_values.append('{}/local.json'.format(ENV_VARS_DIR))

config = ConfigManager.read_configs(config_values)
