from hestia.service_interface import LazyServiceWrapper

from auditor.manager import default_manager
from auditor.service import AuditorService

backend = LazyServiceWrapper(
    backend_base=AuditorService,
    backend_path='auditor.service.AuditorService',
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe
