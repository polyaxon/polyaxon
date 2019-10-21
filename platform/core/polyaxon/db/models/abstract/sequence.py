from django.db import models


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

    def _set_sequence(self, filter_query) -> None:
        if self.pk is None:
            last = filter_query.last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1
