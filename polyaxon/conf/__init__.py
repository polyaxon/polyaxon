from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from conf.service import ConfService


def get_access_backend():
    return settings.CONF_BACKEND or 'conf.service.ConfService'


backend = LazyServiceWrapper(
    backend_base=ConfService,
    backend_path=get_access_backend(),
    options={}
)
backend.expose(locals())
