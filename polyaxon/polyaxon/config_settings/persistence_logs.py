from polyaxon.config_manager import config

PERSISTENCE_LOGS = config.get_dict('POLYAXON_PERSISTENCE_LOGS')
LOGS_MOUNT_PATH = PERSISTENCE_LOGS['mountPath']
LOGS_HOST_PATH = PERSISTENCE_LOGS.get('host_path', LOGS_MOUNT_PATH)
LOGS_CLAIM_NAME = PERSISTENCE_LOGS.get('existingClaim')
