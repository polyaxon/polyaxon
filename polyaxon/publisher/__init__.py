from publisher.service import PublisherService
from libs.services import LazyServiceWrapper

MESSAGES_COUNT = 50
MESSAGES_TIMEOUT = 5

backend = LazyServiceWrapper(
    backend_base=PublisherService,
    backend_path='publisher.service.PublisherService',
    options={}
)
backend.expose(locals())
