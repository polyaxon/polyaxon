from django.conf import settings
from hestia.service_interface import LazyServiceWrapper

from auditor.manager import default_manager
from auditor.service import AuditorService


def get_access_backend():
    return settings.AUDITOR_BACKEND or 'auditor.service.AuditorService'


backend = LazyServiceWrapper(
    backend_base=AuditorService,
    backend_path=get_access_backend(),
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe
