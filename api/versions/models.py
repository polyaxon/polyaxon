# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from django.db import models
from django.core.cache import cache

from libs.models import DiffModel


class BaseVersion(DiffModel):
    """A base model to represents a version singleton."""
    LATEST_VERSION = None
    MIN_VERSION = None

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
    def may_be_update(cls, obj):
        if (obj.latest_version != cls.LATEST_VERSION or
                obj.min_version != cls.MIN_VERSION):
            obj.min_version = settings.MIN_VERSION
            obj.latest_version = settings.LATEST_VERSION
            obj.save()
        obj.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(
                pk=1,
                min_version=settings.CLI_MIN_VERSION,
                latest_version=settings.CLI_LATEST_VERSION_VERSION)
            if not created:
                cls.may_be_update(obj)

        obj = cache.get(cls.__name__)
        return obj


class CliVersion(BaseVersion):
    """A model that represents the polyaxon cli version."""
    LATEST_VERSION = settings.CLI_LATEST_VERSION
    MIN_VERSION = settings.CLI_MIN_VERSION


class PlatformVersion(BaseVersion):
    """A model that represents the polyaxon platfom version."""
    LATEST_VERSION = settings.PLATFORM_LATEST_VERSION
    MIN_VERSION = settings.PLATFORM_MIN_VERSION
