from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from executor.manager import default_manager
from executor.service import BaseExecutorService


def get_executor_backend():
    if settings.ENABLE_SCHEDULER:
        return 'executor.executor_service.ExecutorService'
    return 'executor.service.BaseExecutorService'


backend = LazyServiceWrapper(
    backend_base=BaseExecutorService,
    backend_path=get_executor_backend(),
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe
