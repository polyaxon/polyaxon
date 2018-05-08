from django.conf import settings

from tracker.manager import default_manager
from tracker.service import AnalyticService
from libs.services import LazyServiceWrapper


def get_tracker_backend():
    if settings.ANALYTICS_BACKEND == settings.ANALYTICS_BACKEND_NOOP:
        return 'tracker.service.AnalyticService'
    if settings.ANALYTICS_BACKEND == settings.ANALYTICS_BACKEND_PUBLISHER:
        return 'tracker.publisher.PublisherAnalyticsService'
    return ''


backend = LazyServiceWrapper(
    backend_base=AnalyticService,
    backend_path=get_tracker_backend(),
    options={}
)
backend.expose(locals())

subscribe = default_manager.subscribe
