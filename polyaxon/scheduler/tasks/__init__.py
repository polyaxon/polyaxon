from hestia.imports import import_submodules

import_submodules(globals(), __name__, __path__)

from logs_handlers.tasks import *  # noqa
