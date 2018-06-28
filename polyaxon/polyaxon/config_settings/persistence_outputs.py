import json

from polyaxon.config_manager import config

PERSISTENCE_OUTPUTS = json.loads(config.get_string('POLYAXON_PERSISTENCE_OUTPUTS'))
