from query.service import QueryService
from libs.services import LazyServiceWrapper

backend = LazyServiceWrapper(
    backend_base=QueryService,
    backend_path='query.service.QueryService',
    options={}
)
backend.expose(locals())
