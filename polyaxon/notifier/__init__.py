from libs.services import LazyServiceWrapper
from notifier.managers import default_event_manager, default_action_manager
from notifier.service import NotifierService

backend = LazyServiceWrapper(
    backend_base=NotifierService,
    backend_path='notifier.service.NotifierService',
    options={}
)
backend.expose(locals())

subscribe_event = default_event_manager.subscribe
subscribe_action = default_action_manager.subscribe
