from auditor.manager import default_manager
from auditor.service import AuditorService
from libs.services import LazyServiceWrapper
from polyaxon.utils import config

backend = LazyServiceWrapper(
    backend_base=AuditorService,
    backend_path='auditor.service.AuditorService',
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe

if not config.is_testing:
    setup()
