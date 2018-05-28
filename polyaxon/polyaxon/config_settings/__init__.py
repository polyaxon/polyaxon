from .admin import *
from .celery_settings import *
from .context_processors import *
from .core import *
from .debug import *
from .logging import *
from .secrets import *
from .versions import *
from .tracker import *

from polyaxon.utils import config

if config.is_monolith_service:
    from .monolith import *
elif config.is_api_service:
    from .monolith import *
elif config.is_dockerizer_service:
    from .dockerizer import *
elif config.is_crons_service:
    from .crons import *
elif config.is_namespace_monitor_service:
    from .namespace_monitor import *
elif config.is_resources_monitor_service:
    from .resources_monitor import *
elif config.is_statuses_monitor_service:
    from .statuses_monitor import *
elif config.is_statuses_monitor_service:
    from .statuses_monitor import *
elif config.is_sidecar_service:
    from .sidecar import *
elif config.is_streams_service:
    from .streams import *
elif config.is_hpsearch_service:
    from .streams import *
