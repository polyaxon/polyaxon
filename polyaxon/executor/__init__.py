from hestia.service_interface import LazyServiceWrapper

from executor.manager import default_manager
from executor.service import ExecutorService

backend = LazyServiceWrapper(
    backend_base=ExecutorService,
    backend_path='executor.service.ExecutorService',
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe
