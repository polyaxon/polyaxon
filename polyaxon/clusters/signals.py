from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import auditor

from event_manager.events.cluster import CLUSTER_CREATED
from libs.decorators import ignore_raw, ignore_updates
from models.clusters import Cluster


@receiver(post_save, sender=Cluster, dispatch_uid="cluster_created")
@ignore_updates
@ignore_raw
def cluster_created(sender, **kwargs):
    auditor.record(event_type=CLUSTER_CREATED,
                   instance=kwargs['instance'],
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
