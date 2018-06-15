import uuid

from django.core.cache import cache
from django.core.validators import validate_slug
from django.db import models

from libs.blacklist import validate_blacklist_name


class DescribableModel(models.Model):
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def has_description(self):
        return bool(self.description)


class NameableModel(models.Model):
    name = models.CharField(
        max_length=256,
        validators=[validate_slug, validate_blacklist_name])

    class Meta:
        abstract = True

    def _set_name(self, unique_name):
        if self.pk is None and not self.name:
            self.name = unique_name


class SequenceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('sequence')


class SequenceModel(models.Model):
    sequence = models.PositiveSmallIntegerField(
        editable=False,
        null=False)

    objects = models.Manager()
    sequence_objects = SequenceManager()

    class Meta:
        abstract = True

    def _set_sequence(self, filter_query):
        if self.pk is None:
            last = filter_query.last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1


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

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):  # pylint:disable=arguments-differ
        pass

    @classmethod
    def may_be_update(cls, obj):
        raise NotImplementedError  # noqa

    @classmethod
    def load(cls):
        raise NotImplementedError  # noqa


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
    def last_status(self):
        raise NotImplemented  # noqa

    @property
    def is_running(self):
        return self.STATUSES.is_running(self.last_status)

    @property
    def is_done(self):
        return self.STATUSES.is_done(self.last_status)

    @property
    def failed(self):
        return self.STATUSES.failed(self.last_status)

    @property
    def succeeded(self):
        return self.STATUSES.succeeded(self.last_status)

    @property
    def stopped(self):
        return self.STATUSES.stopped(self.last_status)

    @property
    def finished_at(self):
        raise NotImplemented  # noqa

    @property
    def started_at(self):
        raise NotImplemented  # noqa

    def set_status(self, status, message=None, **kwargs):
        raise NotImplemented  # noqa
