# Default configs
from polyaxon.config_manager import config

from .admin import *
from .api_host import *
from .celery_settings import *
from .context_processors import *
from .core import *
from .email import *
from .integrations import *
from .logging import *
from .oauth import *
from .ownership import *
from .redis_settings import *
from .secrets import *
from .tracker import *
from .versions import *

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
elif config.is_monitor_statuses_service:
    from .monitor_statuses import *
elif config.is_scheduler_service:
    from .scheduler import *
elif config.is_sidecar_service:
    from .sidecar import *
elif config.is_streams_service:
    from .streams import *
elif config.is_hpsearch_service:
    from .hpsearch import *
elif config.is_events_handlers_service:
    from .events_handlers import *
elif config.is_k8s_events_handlers_service:
    from .k8s_events_handlers import *
elif config.is_logs_handlers_service:
    from .logs_handlers import *
