from db.models.config_maps import K8SConfigMap


def register(admin_register):
    admin_register(K8SConfigMap)
