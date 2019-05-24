from django.db import models

from db.models.abstract.diff import DiffModel


class Config(DiffModel):
    owner = models.OneToOneField(
        'db.Owner',
        related_name='config',
        on_delete=models.CASCADE)
    datasets = models.ManyToManyField(
        'db.DataStore',
        blank=True,
        related_name='+')
    artifacts = models.ForeignKey(
        'db.ArtifactsStore',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None)
    logs = models.ForeignKey(
        'db.LogsStore',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None)
    registry = models.ForeignKey(
        'db.Registry',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None)
    k8s_config_maps = models.ManyToManyField(
        'db.K8SConfigMap',
        blank=True,
        related_name='+')
    k8s_secrets = models.ManyToManyField(
        'db.K8SSecret',
        blank=True,
        related_name='+')

    class Meta:
        app_label = 'db'
