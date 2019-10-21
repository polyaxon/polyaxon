def set_tags(instance):
    if not instance.tags and instance.specification:
        instance.tags = instance.specification.tags
