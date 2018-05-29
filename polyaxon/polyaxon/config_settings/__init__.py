# Default configs
from .celery_settings import *
from .context_processors import *
from .core import *
from .debug import *
from .logging import *
from .secrets import *
from .redis_settings import *
from .tracker import *
from .versions import *

from polyaxon.utils import config

# Service configs
if config.is_monolith_service:
    from .monolith import *
elif config.is_api_service:
    from .monolith import *
elif config.is_dockerizer_service:
    from .dockerizer import *
elif config.is_commands_service:
    from .commands import *
elif config.is_crons_service:
    from .crons import *
elif config.is_monitor_namespace_service:
    from .monitor_namespace import *
elif config.is_monitor_resources_service:
    from .monitor_resources import *
elif config.is_scheduler_service:
    from .scheduler import *
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
