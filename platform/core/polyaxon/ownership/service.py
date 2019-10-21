from typing import Any

from hestia.service_interface import Service

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import InterfaceError, OperationalError, ProgrammingError

from options.registry.ownership import ALLOW_USER_OWNERSHIP
from ownership import OwnershipError


class OwnershipService(Service):
    __all__ = (
        'set_owner',
        'set_default_owner',
        'create_owner',
        'delete_owner',
        'validate_owner_name',
    )

    def __init__(self):
        self.content_type_manager = None
        self.owner_manager = None
        self._cluster_owner = None

    @property
    def cluster_owner(self) -> 'Owner':
        if self._cluster_owner:
            return self._cluster_owner

        from db.models.clusters import Cluster

        try:
            cluster = Cluster.load()
            self._cluster_owner = cluster.get_or_create_owner(cluster)
        except (Cluster.DoesNotExist, InterfaceError, ProgrammingError, OperationalError):
            pass
        return self._cluster_owner

    @staticmethod
    def check_owner_type(owner: Any = None, owner_type: str = None) -> None:
        owner_type = owner.owner_type if owner else owner_type
        if not owner_type or owner_type not in settings.OWNER_TYPES:
            raise OwnershipError('Received an invalid owner type `{}`.'.format(owner.owner_type))

    def _set_user_owner(self, instance: Any):
        import conf

        if conf.get(ALLOW_USER_OWNERSHIP):
            try:
                self.set_owner(instance=instance, owner_obj=instance.user)
            except OwnershipError:
                raise OwnershipError('You are not allowed to create {}, '
                                     'please contact your admin.'.format(instance))
        else:
            raise OwnershipError('You are not allowed to create {}, '
                                 'please contact your admin.'.format(instance))

    def _set_cluster_owner(self, instance: Any):
        try:
            self.set_owner(instance=instance, owner=self.cluster_owner)
        except OwnershipError:
            raise OwnershipError('You are not allowed to create {}, '
                                 'please contact your admin.'.format(instance))

    def set_default_owner(self, instance: Any, use_cluster_owner=False) -> None:
        if use_cluster_owner:
            self._set_cluster_owner(instance=instance)
        else:
            self._set_user_owner(instance=instance)

    def set_owner(self, instance: Any,
                  owner: Any = None,
                  owner_name: str = None,
                  owner_obj: Any = None,
                  commit: bool = False) -> None:
        if owner:
            owner = owner
        elif owner_name:
            try:
                owner = self.owner_manager.get(name=owner_name)
            except ObjectDoesNotExist:
                raise OwnershipError('Could not set an owner, owner name not found.')
        elif owner_obj:
            try:
                owner = self.owner_manager.get(
                    object_id=owner_obj.id,
                    content_type_id=self.content_type_manager.get_for_model(owner_obj).id)
            except ObjectDoesNotExist:
                raise OwnershipError('Could not set an owner, owner name not found.')

        self.check_owner_type(owner=owner)
        instance.owner = owner
        if commit:
            instance.save(update_fields=['object_id', 'content_type_id'])

    def create_owner(self, owner_obj: Any, name: str) -> None:
        self.owner_manager.create(
            name=name,
            object_id=owner_obj.id,
            content_type_id=self.content_type_manager.get_for_model(owner_obj).id)

    def delete_owner(self, name: str) -> None:
        try:
            self.owner_manager.get(name=name).delete()
        except ObjectDoesNotExist:
            # Fail silently
            pass

    def validate_owner_name(self, name: str) -> None:
        if self.owner_manager.filter(name__iexact=name).exists():
            raise ValidationError('The name is a reserved word or already taken.')

    def setup(self) -> None:
        super().setup()
        from db.models.owner import Owner
        from django.contrib.contenttypes.models import ContentType

        self.owner_manager = Owner.objects
        self.content_type_manager = ContentType.objects
        self._cluster_owner = None
