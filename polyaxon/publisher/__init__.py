from hestia.service_interface import LazyServiceWrapper

from publisher.service import PublisherService

MESSAGES_COUNT = 50
MESSAGES_TIMEOUT = 5
MESSAGES_TIMEOUT_SHORT = 2

backend = LazyServiceWrapper(
    backend_base=PublisherService,
    backend_path='publisher.service.PublisherService',
    options={}
)
backend.expose(locals())

ERROR = 'ERROR'
