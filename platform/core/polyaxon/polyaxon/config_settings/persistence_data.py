from polyaxon.config_manager import config

PERSISTENCE_DATA = config.get_dict_of_dicts('POLYAXON_PERSISTENCE_DATA')
