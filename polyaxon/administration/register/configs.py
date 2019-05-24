from db.models.configs import Config


def register(admin_register):
    admin_register(Config)
