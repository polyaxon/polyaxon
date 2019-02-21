from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from ci.service import CIService


def get_ci_backend():
    return settings.CI_BACKEND or 'ci.service.CIService'


backend = LazyServiceWrapper(
    backend_base=CIService,
    backend_path=get_ci_backend(),
    options={}
)
backend.expose(locals())
