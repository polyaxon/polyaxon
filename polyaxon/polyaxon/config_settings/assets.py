# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.utils import ROOT_DIR, config

MEDIA_ROOT = config.get_string('POLYAXON_MEDIA_ROOT')
MEDIA_URL = config.get_string('POLYAXON_MEDIA_URL')

STATIC_ROOT = config.get_string('POLYAXON_STATIC_ROOT')
STATIC_URL = config.get_string('POLYAXON_STATIC_URL')

UPLOAD_ROOT = config.get_string('POLYAXON_MOUNT_PATHS_UPLOAD')
DATA_ROOT = config.get_string('POLYAXON_MOUNT_PATHS_DATA')
LOGS_ROOT = config.get_string('POLYAXON_MOUNT_PATHS_LOGS')
OUTPUTS_ROOT = config.get_string('POLYAXON_MOUNT_PATHS_OUTPUTS')
REPOS_ROOT = config.get_string('POLYAXON_MOUNT_PATHS_REPOS')

UPLOAD_CLAIM_NAME = config.get_string('POLYAXON_CLAIM_NAMES_UPLOAD')
DATA_CLAIM_NAME = config.get_string('POLYAXON_CLAIM_NAMES_DATA')
LOGS_CLAIM_NAME = config.get_string('POLYAXON_CLAIM_NAMES_LOGS')
OUTPUTS_CLAIM_NAME = config.get_string('POLYAXON_CLAIM_NAMES_OUTPUTS')
REPOS_CLAIM_NAME = config.get_string('POLYAXON_CLAIM_NAMES_REPOS')

# TODO: intergrate subpaths
UPLOAD_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_UPLOAD', is_optional=True)
DATA_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_DATA', is_optional=True)
LOGS_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_LOGS', is_optional=True)
OUTPUTS_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_OUTPUTS', is_optional=True)
REPOS_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_REPOS', is_optional=True)

# Additional locations of static files
STATICFILES_DIRS = (
    ROOT_DIR.child('client').child('public'),
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
