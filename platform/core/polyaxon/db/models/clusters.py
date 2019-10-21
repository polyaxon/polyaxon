import uuid

from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models

from db.models.abstract.singleton import SingletonModel
from options.registry.deployments import (
    CHART_IS_UPGRADE,
    CHART_VERSION,
    CLI_LATEST_VERSION,
    CLI_MIN_VERSION,
    PLATFORM_LATEST_VERSION,
    PLATFORM_MIN_VERSION,
    POLYAXON_ENVIRONMENT
)
from options.registry.k8s import K8S_NAMESPACE


class Cluster(SingletonModel):
    """A model that represents the cluster api version."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    version_api = JSONField(help_text='The cluster version api info')

    class Meta:
        app_label = 'db'

    def __str__(self):
        return 'Cluster: {}'.format(self.uuid.hex)

    @staticmethod
    def record(obj: 'Cluster') -> None:
        import auditor
        import conf

        from events.registry.cluster import CLUSTER_CREATED

        auditor.record(
            event_type=CLUSTER_CREATED,
            instance=obj,
            namespace=conf.get(K8S_NAMESPACE),
            environment=conf.get(POLYAXON_ENVIRONMENT),
            is_upgrade=conf.get(CHART_IS_UPGRADE),
            cli_min_version=conf.get(CLI_MIN_VERSION),
            cli_latest_version=conf.get(CLI_LATEST_VERSION),
            platform_min_version=conf.get(PLATFORM_LATEST_VERSION),
            platform_latest_version=conf.get(PLATFORM_MIN_VERSION),
            chart_version=conf.get(CHART_VERSION))

    @classmethod
    def may_be_update(cls, obj: 'Cluster') -> None:
        pass

    @staticmethod
    def create_cluster_owner(cluster):
        from db.models.owner import Owner
        from django.contrib.contenttypes.models import ContentType

        owner, _ = Owner.objects.get_or_create(
            object_id=cluster.id,
            content_type_id=ContentType.objects.get_for_model(cluster).id)
        if owner.name != cluster.uuid.hex:
            owner.name = cluster.uuid.hex
            owner.save(update_fields=['name'])

        return owner

    @staticmethod
    def get_or_create_owner(cluster):
        from db.models.owner import Owner

        try:
            return Owner.objects.get(name=cluster.uuid.hex)
        except Owner.DoesNotExist:
            return cluster.create_cluster_owner(cluster)

    @classmethod
    def load(cls) -> 'Cluster':

        if cache.get(cls.__name__) is None:
            try:
                obj = cls.objects.get(pk=1)
            except cls.DoesNotExist:
                params = {'version_api': {}}
                obj = cls.objects.create(pk=1, **params)
                obj.set_cache()
                cls.record(obj)
                cls.create_cluster_owner(obj)
        else:
            obj = cache.get(cls.__name__)
        return obj
