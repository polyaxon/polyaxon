from hestia.service_interface import LazyServiceWrapper

from access.service import AccessService


backend = LazyServiceWrapper(
    backend_base=AccessService,
    backend_path='access.service.AccessService',
    options={}
)
backend.expose(locals())
