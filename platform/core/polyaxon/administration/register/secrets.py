from db.models.secrets import K8SSecret


def register(admin_register):
    admin_register(K8SSecret)
