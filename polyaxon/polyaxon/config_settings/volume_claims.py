import json

from polyaxon.utils import config

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

REPOS_ARCHIVE_ROOT = '/tmp/archived_repos'
