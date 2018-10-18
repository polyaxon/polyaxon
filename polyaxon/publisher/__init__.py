from libs.services import LazyServiceWrapper
from publisher import log_spec
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

LogSpec = log_spec.log_spec

ERROR = 'ERROR'
DATETIME_FORMAT = log_spec.DATETIME_FORMAT
