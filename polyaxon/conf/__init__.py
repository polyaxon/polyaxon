from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from conf.service import ConfService


def get_conf_backend():
    return settings.CONF_BACKEND or 'conf.service.ConfService'


backend = LazyServiceWrapper(
    backend_base=ConfService,
    backend_path=get_conf_backend(),
    options={}
)
backend.expose(locals())
