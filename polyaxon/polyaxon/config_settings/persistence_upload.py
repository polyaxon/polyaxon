import json

from polyaxon.config_manager import config

PERSISTENCE_UPLOAD = json.loads(config.get_string('POLYAXON_PERSISTENCE_UPLOAD'))
UPLOAD_ROOT = PERSISTENCE_UPLOAD['mountPath']
UPLOAD_CLAIM_NAME = PERSISTENCE_UPLOAD.get('existingClaim')
