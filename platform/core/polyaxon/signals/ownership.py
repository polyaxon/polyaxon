from hestia.signal_decorators import ignore_raw, ignore_updates_pre

from django.db.models.signals import pre_save
from django.dispatch import receiver

import ownership

from db.models.artifacts_stores import ArtifactsStore
from db.models.config_maps import K8SConfigMap
from db.models.data_stores import DataStore
from db.models.git_access import GitAccess
from db.models.logs_stores import LogsStore
from db.models.projects import Project
from db.models.registry_access import RegistryAccess
from db.models.secrets import K8SSecret


@receiver(pre_save, sender=Project, dispatch_uid="project_pre_save")
@ignore_updates_pre
@ignore_raw
def project_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance)


@receiver(pre_save, sender=K8SConfigMap, dispatch_uid="k8s_config_map_pre_save")
@ignore_updates_pre
@ignore_raw
def k8s_config_map_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance, use_cluster_owner=True)


@receiver(pre_save, sender=K8SSecret, dispatch_uid="k8s_secrets_pre_save")
@ignore_updates_pre
@ignore_raw
def k8s_secrets_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance, use_cluster_owner=True)


@receiver(pre_save, sender=DataStore, dispatch_uid="data_store_pre_save")
@ignore_updates_pre
@ignore_raw
def data_store_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance, use_cluster_owner=True)


@receiver(pre_save, sender=LogsStore, dispatch_uid="logs_store_pre_save")
@ignore_updates_pre
@ignore_raw
def logs_store_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance, use_cluster_owner=True)


@receiver(pre_save, sender=ArtifactsStore, dispatch_uid="artifacts_store_pre_save")
@ignore_updates_pre
@ignore_raw
def artifacts_store_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance, use_cluster_owner=True)


@receiver(pre_save, sender=GitAccess, dispatch_uid="git_access_pre_save")
@ignore_updates_pre
@ignore_raw
def git_access_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance, use_cluster_owner=True)


@receiver(pre_save, sender=RegistryAccess, dispatch_uid="registry_access_pre_save")
@ignore_updates_pre
@ignore_raw
def registry_access_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.has_owner:
        ownership.set_default_owner(instance=instance, use_cluster_owner=True)
