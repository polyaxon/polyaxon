from polyaxon.config_manager import config

PERSISTENCE_OUTPUTS = config.get_dict_of_dicts('POLYAXON_PERSISTENCE_OUTPUTS')
