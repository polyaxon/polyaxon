# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from api.utils import config

from .apps import INSTALLED_APPS, MIDDLEWARE_CLASSES

if config.get_boolean('POLYAXON_DEBUG', is_optional=True):

    def show_toolbar(request):
        # debug toolbar makes import take VERY long (because of SQL traces) and can break tests
        if request.path.endswith('upload') or 'test' in sys.argv:
            return False
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
        'INTERCEPT_REDIRECTS': False,
        'HIDE_DJANGO_SQL': False,
        'ENABLE_STACKTRACES': True,
    }

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
    )

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )
