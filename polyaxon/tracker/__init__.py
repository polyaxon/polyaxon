from django.conf import settings

from tracker.manager import default_manager
from tracker.service import TrackerService
from libs.services import LazyServiceWrapper


def get_tracker_backend():
    if settings.TRACKER_BACKEND == settings.TRACKER_BACKEND_NOOP:
        return 'tracker.service.TrackerService'
    if settings.TRACKER_BACKEND == settings.TRACKER_BACKEND_PUBLISHER:
        return 'tracker.publisher.PublisherService'
    return ''


backend = LazyServiceWrapper(
    backend_base=TrackerService,
    backend_path=get_tracker_backend(),
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe
