from hestia.service_interface import LazyServiceWrapper

from query.service import QueryService

backend = LazyServiceWrapper(
    backend_base=QueryService,
    backend_path='query.service.QueryService',
    options={}
)
backend.expose(locals())
