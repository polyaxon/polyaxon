from django.db import models


class SecretModel(models.Model):
    k8s_secret = models.ForeignKey(
        'db.K8SSecret',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    db_secret = models.ForeignKey(
        'db.ConfigOption',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')

    class Meta:
        abstract = True
