# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

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

# TODO: integrate subpaths
UPLOAD_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_UPLOAD', is_optional=True)
DATA_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_DATA', is_optional=True)
LOGS_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_LOGS', is_optional=True)
OUTPUTS_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_OUTPUTS', is_optional=True)
REPOS_SUB_PATHS = config.get_string('POLYAXON_SUB_PATHS_REPOS', is_optional=True)

# Extra persistence volumes
EXTRA_PERSISTENCES = config.get_string('POLYAXON_EXTRA_PERSISTENCES', is_optional=True)
if EXTRA_PERSISTENCES:
    EXTRA_PERSISTENCES = json.loads(EXTRA_PERSISTENCES)

# EXTRA_PV_SLOTS_COUNT = 5
#
# EXTRA_MOUNT_PATH_1 = config.get_string('POLYAXON_MOUNT_PATHS_EXTRA_1', is_optional=True)
# EXTRA_CLAIM_NAME_1 = config.get_string('POLYAXON_CLAIM_NAMES_EXTRA_1', is_optional=True)
# EXTRA_HOST_PATH_1 = config.get_string('POLYAXON_HOST_PATH_EXTRA_1', is_optional=True)
#
# EXTRA_MOUNT_PATH_2 = config.get_string('POLYAXON_MOUNT_PATHS_EXTRA_2', is_optional=True)
# EXTRA_CLAIM_NAME_2 = config.get_string('POLYAXON_CLAIM_NAMES_EXTRA_2', is_optional=True)
# EXTRA_HOST_PATH_2 = config.get_string('POLYAXON_HOST_PATH_EXTRA_2', is_optional=True)
#
# EXTRA_MOUNT_PATH_3 = config.get_string('POLYAXON_MOUNT_PATHS_EXTRA_3', is_optional=True)
# EXTRA_CLAIM_NAME_3 = config.get_string('POLYAXON_CLAIM_NAMES_EXTRA_3', is_optional=True)
# EXTRA_HOST_PATH_3 = config.get_string('POLYAXON_HOST_PATH_EXTRA_3', is_optional=True)
#
# EXTRA_MOUNT_PATH_4 = config.get_string('POLYAXON_MOUNT_PATHS_EXTRA_4', is_optional=True)
# EXTRA_CLAIM_NAME_4 = config.get_string('POLYAXON_CLAIM_NAMES_EXTRA_4', is_optional=True)
# EXTRA_HOST_PATH_4 = config.get_string('POLYAXON_HOST_PATH_EXTRA_4', is_optional=True)
#
# EXTRA_MOUNT_PATH_5 = config.get_string('POLYAXON_MOUNT_PATHS_EXTRA_5', is_optional=True)
# EXTRA_CLAIM_NAME_5 = config.get_string('POLYAXON_CLAIM_NAMES_EXTRA_5', is_optional=True)
# EXTRA_HOST_PATH_5 = config.get_string('POLYAXON_HOST_PATH_EXTRA_5', is_optional=True)

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
