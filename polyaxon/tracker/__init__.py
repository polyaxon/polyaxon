from django.conf import settings

from libs.services import LazyServiceWrapper
from polyaxon.utils import config
from tracker.manager import default_manager
from tracker.service import TrackerService


def get_tracker_backend():
    if settings.TRACKER_BACKEND == settings.TRACKER_BACKEND_NOOP:
        return 'tracker.service.TrackerService'
    if settings.TRACKER_BACKEND == settings.TRACKER_BACKEND_PUBLISHER:
        return 'tracker.publish_tracker.PublishTrackerService'
    return ''


def get_backend_options():
    if settings.TRACKER_BACKEND == settings.TRACKER_BACKEND_NOOP:
        return {}
    if settings.TRACKER_BACKEND == settings.TRACKER_BACKEND_PUBLISHER:
        return {'key': config.tracker_key}
    return {}


backend = LazyServiceWrapper(
    backend_base=TrackerService,
    backend_path=get_tracker_backend(),
    options=get_backend_options()
)
backend.expose(locals())

subscribe = default_manager.subscribe

if not config.is_testing:
    setup()
