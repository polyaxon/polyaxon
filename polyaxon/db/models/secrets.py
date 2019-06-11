from django.contrib.postgres.fields import ArrayField
from django.db import models

from db.models.abstract.access_catalog import Catalog


class K8SSecret(Catalog):
    """A model to represent a catalog of k8s secrets.

    Since k8s secrets can hold several entries,
    often time the user only requires mounting some of these keys.

    N.B. If no keys are specified, the whole secret will be mounted to the requiting jobs.
    """
    secret_ref = models.CharField(max_length=256)
    keys = ArrayField(models.CharField(max_length=256), default=list, blank=True)

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)
