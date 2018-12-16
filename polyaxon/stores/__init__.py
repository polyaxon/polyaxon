from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from stores.service import StoresService


def get_paths_backend():
    return settings.ACCESS_BACKEND or 'stores.service.StoresService'


backend = LazyServiceWrapper(
    backend_base=StoresService,
    backend_path=get_paths_backend(),
    options={}
)
backend.expose(locals())
