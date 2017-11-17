# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import ROOT_DIR, config

MEDIA_ROOT = config.get_string('POLYAXON_MEDIA_ROOT')
MEDIA_URL = config.get_string('POLYAXON_MEDIA_URL')

STATIC_ROOT = config.get_string('POLYAXON_STATIC_ROOT')
STATIC_URL = config.get_string('POLYAXON_STATIC_URL')


# Additional locations of static files
STATICFILES_DIRS = (
    ROOT_DIR.child('client'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOCALE_PATHS = (
    ROOT_DIR.child('locale'),
    ROOT_DIR.child('client').child('js').child('libs').child('locale')
)

STATICI18N_ROOT = 'static'
STATICI18N_OUTPUT_DIR = 'jsi18n'
