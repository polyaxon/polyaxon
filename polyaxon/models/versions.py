from django.conf import settings
from django.core.cache import cache
from django.db import models

from libs.models import Singleton


class BaseValidationVersion(Singleton):
    LATEST_VERSION = None
    MIN_VERSION = None

    latest_version = models.CharField(max_length=16)
    min_version = models.CharField(max_length=16)

    class Meta:
        abstract = True

    @classmethod
    def may_be_update(cls, obj):
        if obj.latest_version != cls.LATEST_VERSION or obj.min_version != cls.MIN_VERSION:
            obj.min_version = cls.MIN_VERSION
            obj.latest_version = cls.LATEST_VERSION
            obj.save()
            obj.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            try:
                obj = cls.objects.get(pk=1)
            except cls.DoesNotExist:
                obj = cls.objects.create(
                    pk=1,
                    min_version=settings.CLI_MIN_VERSION,
                    latest_version=settings.CLI_LATEST_VERSION)
                obj.set_cache()
        else:
            obj = cache.get(cls.__name__)

        cls.may_be_update(obj)
        return obj


class CliVersion(BaseValidationVersion):
    """A model that represents the polyaxon cli version."""
    LATEST_VERSION = settings.CLI_LATEST_VERSION
    MIN_VERSION = settings.CLI_MIN_VERSION

    class Meta:
        app_label = 'polyaxon'

    def __str__(self):
        return 'Cli version'


class PlatformVersion(BaseValidationVersion):
    """A model that represents the polyaxon platform version."""
    LATEST_VERSION = settings.PLATFORM_LATEST_VERSION
    MIN_VERSION = settings.PLATFORM_MIN_VERSION

    class Meta:
        app_label = 'polyaxon'

    def __str__(self):
        return 'Platform version'


class LibVersion(BaseValidationVersion):
    """A model that represents the polyaxon lib version."""
    LATEST_VERSION = settings.LIB_LATEST_VERSION
    MIN_VERSION = settings.LIB_MIN_VERSION

    class Meta:
        app_label = 'polyaxon'

    def __str__(self):
        return 'Lib version'


class ChartVersion(Singleton):
    """A model that represents the polyaxon chart version."""
    VERSION = settings.CHART_VERSION

    version = models.CharField(max_length=16)

    class Meta:
        app_label = 'polyaxon'

    def __str__(self):
        return 'Chart version'

    @classmethod
    def may_be_update(cls, obj):
        if obj.version != cls.VERSION:
            obj.version = cls.VERSION
            obj.save()
        obj.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            try:
                obj = cls.objects.get(pk=1)
            except cls.DoesNotExist:
                obj = cls.objects.create(pk=1, version=cls.VERSION)
        else:
            obj = cache.get(cls.__name__)

        cls.may_be_update(obj)
        return obj
