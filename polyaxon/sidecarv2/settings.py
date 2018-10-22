import os
import rhea

config = rhea.Rhea.read_configs([
    os.environ,
])

MESSAGES_COUNT = config.get_string('POLYAXON_MESSAGES_COUNT',
                                   is_optional=True,
                                   default=50)
MESSAGES_TIMEOUT = config.get_string('POLYAXON_MESSAGES_TIMEOUT',
                                     is_optional=True,
                                     default=5)
MESSAGES_TIMEOUT_SHORT = config.get_string('POLYAXON_MESSAGES_TIMEOUT_SHORT',
                                           is_optional=True,
                                           default=2)
