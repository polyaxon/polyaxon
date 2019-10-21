import uuid

from typing import Dict, Optional

from hestia.datetime_typing import AwareDT

from django.db import models
from django.utils import timezone


class StatusModel(models.Model):
    """A model that represents a status at certain time.

    This is an abstract class, every subclass must implement a status attribute,
    it must implement also Foreignkey to the model that needs a status.

    e.g.

    # status = db.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)
    # job = db.ForeignKey(Job, on_delete=db.CASCADE, related_name='statuses')
    """
    STATUSES = None

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    message = models.CharField(max_length=256, null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{} <{}>'.format(str(self), self.status)

    class Meta:
        verbose_name_plural = 'Statuses'
        ordering = ['created_at']
        abstract = True


class LastStatusMixin(object):
    """A mixin that extracts the logic of last_status.

    This is an abstract class, every subclass must implement a status attribute,
    as well as a last_status attribute:

    e.g.

    status = db.OneToOneField(
        'ExperimentStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=db.SET_NULL)
    """
    STATUSES = None

    @property
    def last_status(self) -> Optional[str]:
        if not hasattr(self, 'status'):
            return None
        return self.status.status if self.status else None

    @property
    def is_running(self) -> bool:
        return self.STATUSES.is_running(self.last_status)

    @property
    def is_stoppable(self) -> bool:
        return self.STATUSES.is_stoppable(self.last_status)

    @property
    def is_done(self) -> bool:
        return self.STATUSES.is_done(self.last_status)

    @property
    def failed(self) -> bool:
        return self.STATUSES.failed(self.last_status)

    @property
    def succeeded(self) -> bool:
        return self.STATUSES.succeeded(self.last_status)

    @property
    def done(self) -> bool:
        return self.STATUSES.done(self.last_status)

    @property
    def stopped(self) -> bool:
        return self.STATUSES.stopped(self.last_status)

    def last_status_before(self, status_date: AwareDT) -> str:
        raise NotImplemented  # noqa

    def set_status(self,
                   status: str,
                   created_at: AwareDT = None,
                   message: str = None,
                   traceback: Dict = None,
                   **kwargs) -> None:
        raise NotImplemented  # noqa
