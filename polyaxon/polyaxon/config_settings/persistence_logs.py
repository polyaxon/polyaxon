import json

from polyaxon.config_manager import config

PERSISTENCE_LOGS = json.loads(config.get_string('POLYAXON_PERSISTENCE_LOGS'))
LOGS_ROOT = PERSISTENCE_LOGS['mountPath']
LOGS_CLAIM_NAME = PERSISTENCE_LOGS.get('existingClaim')
