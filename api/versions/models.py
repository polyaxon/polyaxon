# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.db import models
from django.core.cache import cache

from libs.models import DiffModel


class BaseVersion(DiffModel):
    """A base model to represents a version singleton."""
    latest_version = models.CharField(max_length=16)
    min_version = models.CharField(max_length=16)

    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(BaseVersion, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1,
                                                     min_version='0.0.1',
                                                     latest_version='0.0.1')
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class CliVersion(BaseVersion):
    """A model that represents the polyaxon cli version."""
    pass
