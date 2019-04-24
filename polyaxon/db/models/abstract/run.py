import uuid

from django.db import models

from db.models.abstract.deleted import DeletedModel
from db.models.abstract.diff import DiffModel
from db.models.statuses import LastStatusMixin


class RunTimeModel(models.Model):
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class RunModel(DiffModel, RunTimeModel, DeletedModel, LastStatusMixin):
    """
    A model that represents an execution behaviour of instance/run of a operation or a pipeline.
    """
    STATUSES = None

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)

    class Meta:
        abstract = True
