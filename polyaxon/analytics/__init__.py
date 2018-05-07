from django.conf import settings

from analytics.manager import default_manager
from analytics.service import AnalyticService
from libs.services import LazyServiceWrapper
from polyaxon.utils import config


def get_analytics_backend():
    if settings.ANALYTICS_BACKEND == settings.ANALYTICS_BACKEND_NOOP:
        return 'analytics.service.AnalyticService'
    if settings.ANALYTICS_BACKEND == settings.ANALYTICS_BACKEND_PUBLISHER:
        return 'analytics.publisher.PublisherAnalyticsService'
    return ''


backend = LazyServiceWrapper(
    backend_base=AnalyticService,
    backend_path=get_analytics_backend,
    options=config.get_analytics_backend_options()
)
backend.expose(locals())

register = default_manager.register
