import json

from polyaxon.config_manager import config

PERSISTENCE_UPLOAD = json.loads(config.get_string('POLYAXON_PERSISTENCE_UPLOAD'))
UPLOAD_MOUNT_PATH = PERSISTENCE_UPLOAD['mountPath']
UPLOAD_HOST_PATH = PERSISTENCE_UPLOAD.get('host_path', UPLOAD_MOUNT_PATH)
UPLOAD_CLAIM_NAME = PERSISTENCE_UPLOAD.get('existingClaim')
