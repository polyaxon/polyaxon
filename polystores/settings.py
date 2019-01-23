import os

import rhea

config = rhea.Rhea.read_configs([
    os.environ,
])


RUN_STORES_ACCESS_KEYS = config.get_dict('POLYSTORES_RUN_STORES_ACCESS_KEYS',
                                         is_optional=True,
                                         default={})
TMP_AUTH_GCS_ACCESS_PATH = config.get_string('POLYSTORES_TMP_AUTH_GCS_ACCESS_PATH',
                                             is_optional=True,
                                             default='/tmp/.polyaxon/.gcsaccess.json')
