import json

from polyaxon.config_manager import config

PERSISTENCE_REPOS = json.loads(config.get_string('POLYAXON_PERSISTENCE_REPOS'))
REPOS_ROOT = PERSISTENCE_REPOS['mountPath']
REPOS_CLAIM_NAME = PERSISTENCE_REPOS.get('existingClaim')
