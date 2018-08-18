from polyaxon.config_manager import config

from .apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE
from .rest import REST_FRAMEWORK

if config.is_debug_mode and config.is_monolith_service and not config.is_testing_env:
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x: True,
        'INTERCEPT_REDIRECTS': False,
        'HIDE_DJANGO_SQL': False,
        'ENABLE_STACKTRACES': True,
    }

    DEBUG_TOOLBAR_PANELS = (
        # 'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        # 'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        # 'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        # 'debug_toolbar.panels.signals.SignalsPanel',
        # 'debug_toolbar.panels.logging.LoggingPanel',
        # 'debug_toolbar.panels.redirects.RedirectsPanel',
        # 'debug_toolbar.panels.profiling.ProfilingPanel'
    )

    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += ('rest_framework.renderers.BrowsableAPIRenderer',)
