from db.models.config_options import ConfigOption


def register(admin_register):
    admin_register(ConfigOption)
