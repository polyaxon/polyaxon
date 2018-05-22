import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models


from libs.models import Singleton


class Cluster(Singleton):
    """A model that represents the cluster api version."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    version_api = JSONField(help_text='The cluster version api info')

    class Meta:
        app_label = 'polyaxon'

    def __str__(self):
        return 'Cluster: {}'.format(self.uuid.hex)

    @classmethod
    def may_be_update(cls, obj):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            try:
                obj = cls.objects.get(pk=1)
            except cls.DoesNotExist:
                params = {'version_api': {}}
                if settings.CLUSTER_ID:
                    params['uuid'] = settings.CLUSTER_ID
                obj = cls.objects.create(pk=1, **params)
                obj.set_cache()
        else:
            obj = cache.get(cls.__name__)
        return obj
