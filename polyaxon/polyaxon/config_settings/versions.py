from polyaxon.utils import config

CLI_MIN_VERSION = config.get_string('POLYAXON_CLI_MIN_VERSION',
                                    is_optional=True,
                                    default='0.0.0')
CLI_LATEST_VERSION = config.get_string('POLYAXON_CLI_LATEST_VERSION',
                                       is_optional=True,
                                       default='0.0.0')
PLATFORM_MIN_VERSION = config.get_string('POLYAXON_PLATFORM_MIN_VERSION',
                                         is_optional=True,
                                         default='0.0.0')
PLATFORM_LATEST_VERSION = config.get_string('POLYAXON_PLATFORM_LATEST_VERSION',
                                            is_optional=True,
                                            default='0.0.0')
LIB_MIN_VERSION = config.get_string('POLYAXON_LIB_MIN_VERSION',
                                    is_optional=True,
                                    default='0.0.0')
LIB_LATEST_VERSION = config.get_string('POLYAXON_LIB_LATEST_VERSION',
                                       is_optional=True,
                                       default='0.0.0')
CHART_VERSION = config.get_string('POLYAXON_CHART_VERSION',
                                  is_optional=True,
                                  default='0.0.0')
