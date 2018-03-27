import uuid

from django.db import models
from django.core.cache import cache


class DescribableModel(models.Model):
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class DiffModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TypeModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    schema_definition = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Singleton(DiffModel):
    """A base model to represents a singleton."""

    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def may_be_update(cls, obj):
        raise NotImplementedError

    @classmethod
    def load(cls):
        raise NotImplementedError


class StatusModel(models.Model):
    """A model that represents a status at certain time.

    This is an abstract class, every subclass must implement a status attribute,
    it must implement also Foreignkey to the model that needs a status.

    e.g.

    # status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=STATUSES.CREATED,
        choices=STATUSES.CHOICES)
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='statuses')
    """
    STATUSES = None

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    message = models.CharField(max_length=256, null=True, blank=True)

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

    experiment_status = models.OneToOneField(
        'ExperimentStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)
    """
    STATUSES = None

    @property
    def last_status(self):
        raise NotImplemented

    @property
    def is_running(self):
        return self.STATUSES.is_running(self.last_status)

    @property
    def is_done(self):
        return self.STATUSES.is_done(self.last_status)

    @property
    def finished_at(self):
        raise NotImplemented

    @property
    def started_at(self):
        raise NotImplemented

    def set_status(self, status, message=None, **kwargs):
        raise NotImplemented
