from auditor.manager import default_manager
from auditor.service import AuditorService
from libs.services import LazyServiceWrapper


backend = LazyServiceWrapper(
    backend_base=AuditorService,
    backend_path='auditor.service.AuditorService',
    options={}
)
backend.expose(locals())

register = default_manager.register
