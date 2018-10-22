from hestia.service_interface import LazyServiceWrapper

from notifier.managers import default_action_manager, default_event_manager
from notifier.service import NotifierService

backend = LazyServiceWrapper(
    backend_base=NotifierService,
    backend_path='notifier.service.NotifierService',
    options={}
)
backend.expose(locals())

subscribe_event = default_event_manager.subscribe
subscribe_action = default_action_manager.subscribe
