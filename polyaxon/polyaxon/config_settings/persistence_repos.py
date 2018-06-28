import json

from polyaxon.config_manager import config

PERSISTENCE_REPOS = json.loads(config.get_string('POLYAXON_PERSISTENCE_REPOS'))
REPOS_MOUNT_PATH = PERSISTENCE_REPOS['mountPath']
REPOS_HOST_PATH = PERSISTENCE_REPOS.get('host_path', REPOS_MOUNT_PATH)
REPOS_CLAIM_NAME = PERSISTENCE_REPOS.get('existingClaim')
