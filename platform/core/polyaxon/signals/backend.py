def set_backend(instance, default_backend):
    if instance.specification and instance.specification.config.backend:
        instance.backend = instance.specification.config.backend or default_backend
    elif instance.backend is None:
        instance.backend = default_backend
