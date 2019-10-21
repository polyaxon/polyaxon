from hestia.service_interface import LazyServiceWrapper

from django.conf import settings

from access.service import AccessService


def get_access_backend():
    return settings.ACCESS_BACKEND or 'access.service.AccessService'


backend = LazyServiceWrapper(
    backend_base=AccessService,
    backend_path=get_access_backend(),
    options={}
)
backend.expose(locals())
