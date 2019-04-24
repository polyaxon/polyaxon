from django.core.cache import cache

from db.models.abstract.diff import DiffModel


class Singleton(DiffModel):
    """A base model to represents a singleton."""

    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):  # pylint:disable=arguments-differ
        self.pk = 1
        super().save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):  # pylint:disable=arguments-differ
        pass

    @classmethod
    def may_be_update(cls, obj):
        raise NotImplementedError  # noqa

    @classmethod
    def load(cls):
        raise NotImplementedError  # noqa
