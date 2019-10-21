from hestia.imports import import_submodules

from logs_handlers.tasks.log_handlers import *  # noqa
from polyflow.tasks import *  # noqa

import_submodules(globals(), __name__, __path__)
