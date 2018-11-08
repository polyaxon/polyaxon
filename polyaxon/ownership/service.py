from hestia.service_interface import Service

from constants import content_types
from ownership.exceptions import OwnershipError


class OwnershipService(Service):
    __all__ = ('setup', 'get_owner_type', 'has_owner', 'get_owner_type', 'get_owner', 'set_owner')

    def __init__(self):
        self.content_type_manager = None

    @staticmethod
    def get_owner_type(instance):
        return instance.owner_content_type.model

    @classmethod
    def get_owner(cls, instance):
        owner_type = cls.get_owner_type(instance=instance)
        if owner_type == content_types.USER:
            return '{}:{}'.format(owner_type, instance.owner.username)
        raise OwnershipError('This owner type is not supported by your Polyaxon version.')

    @staticmethod
    def has_owner(instance):
        return all([instance.owner_object_id, instance.owner_content_type_id])

    def set_owner(self, instance, owner, commit=False):
        instance.owner_object_id = owner.id
        instance.owner_content_type_id = self.content_type_manager.get_for_model(owner).id
        if commit:
            instance.save(update_fields=['owner_object_id', 'owner_content_type_id'])

    def setup(self):
        super().setup()
        from django.contrib.contenttypes.models import ContentType

        self.content_type_manager = ContentType.objects
