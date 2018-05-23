from publisher.service import PublisherService
from libs.services import LazyServiceWrapper

backend = LazyServiceWrapper(
    backend_base=PublisherService,
    backend_path='publisher.service.PublisherService',
    options={}
)
backend.expose(locals())
