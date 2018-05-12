from activitylogs.manager import default_manager
from activitylogs.service import ActivityLogService
from libs.services import LazyServiceWrapper
from polyaxon.utils import config

backend = LazyServiceWrapper(
    backend_base=ActivityLogService,
    backend_path='activitylogs.service.ActivityLogService',
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe


if not config.is_testing:
    setup()
