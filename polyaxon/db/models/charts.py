import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from db.models.utils import DiffModel, NameableModel


class ChartViewModel(DiffModel, NameableModel):
    """A model that represents a chart view or a group of charts.

    This is an abstract class, every subclass must implement a
    Foreignkey to the model that needs a status.

    e.g.

    # metric = db.ForeignKey(Experiment, on_delete=db.CASCADE, related_name='chart_views')
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    charts = JSONField()
    meta = JSONField(
        null=True,
        blank=True,
        default=dict
    )

    class Meta:
        verbose_name_plural = 'Chart Views'
        ordering = ['created_at']
        abstract = True
