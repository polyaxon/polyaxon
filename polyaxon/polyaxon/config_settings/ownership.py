from polyaxon.config_manager import config

OWNER_TYPES = config.get_string('POLYAXON_OWNER_TYPES',
                                is_optional=True,
                                is_list=True,
                                default=['user'])
ROLES = config.get_dict('POLYAXON_ROLES',
                        is_optional=True,
                        is_list=True,
                        default=[])
DEFAULT_ROLE = config.get_string('POLYAXON_DEFAULT_ROLE',
                                 is_optional=True,
                                 default='dummy')
SCOPE_ROLES = config.get_dict_of_dicts('POLYAXON_SCOPE_ROLES',
                                       is_optional=True,
                                       default={})
