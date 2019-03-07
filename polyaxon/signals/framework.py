def set_framework(instance):
    if instance.specification and instance.specification.config.framework:
        instance.framework = instance.specification.config.framework
