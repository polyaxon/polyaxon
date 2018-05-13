import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models

import auditor

from event_manager.events.cluster import CLUSTER_CREATED
from libs.models import Singleton


class Cluster(Singleton):
    """A model that represents the cluster api version."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    version_api = JSONField(help_text='The cluster version api info')

    def __str__(self):
        return 'Cluster: {}'.format(self.uuid.hex)

    @classmethod
    def may_be_update(cls, obj):
        pass

    @staticmethod
    def record(obj):
        auditor.record(event_type=CLUSTER_CREATED,
                       instance=obj,
                       namespace=settings.K8S_NAMESPACE,
                       environment=settings.POLYAXON_ENVIRONMENT,
                       is_upgrade=settings.CHART_IS_UPGRADE,
                       provisioner_enabled=settings.K8S_PROVISIONER_ENABLED,
                       use_data_claim=bool(settings.DATA_CLAIM_NAME),
                       use_outputs_claim=bool(settings.OUTPUTS_CLAIM_NAME),
                       use_logs_claim=bool(settings.LOGS_CLAIM_NAME),
                       use_repos_claim=bool(settings.REPOS_CLAIM_NAME),
                       use_upload_claim=bool(settings.UPLOAD_CLAIM_NAME),
                       node_selector_core_enabled=bool(settings.NODE_SELECTORS_CORE),
                       node_selector_experiments_enabled=bool(settings.NODE_SELECTORS_EXPERIMENTS),
                       cli_min_version=settings.CLI_MIN_VERSION,
                       cli_latest_version=settings.CLI_LATEST_VERSION,
                       platform_min_version=settings.PLATFORM_LATEST_VERSION,
                       platform_latest_version=settings.PLATFORM_MIN_VERSION,
                       chart_version=settings.CHART_VERSION)

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
                cls.record(obj)
        else:
            obj = cache.get(cls.__name__)
        return obj
