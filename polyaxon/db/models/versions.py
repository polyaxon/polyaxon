from django.core.cache import cache
from django.db import models

from db.models.utils import Singleton


class BaseValidationVersion(Singleton):
    latest_version = models.CharField(max_length=16)
    min_version = models.CharField(max_length=16)

    class Meta:
        abstract = True

    @staticmethod
    def get_min_version():
        raise NotImplementedError

    @staticmethod
    def get_latest_version():
        raise NotImplementedError

    @classmethod
    def may_be_update(cls, obj):
        min_version = cls.get_min_version()
        latest_version = cls.get_latest_version()
        if obj.latest_version != latest_version or obj.min_version != min_version:
            obj.min_version = min_version
            obj.latest_version = latest_version
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
                    min_version=cls.get_min_version(),
                    latest_version=cls.get_latest_version())
                obj.set_cache()
        else:
            obj = cache.get(cls.__name__)

        cls.may_be_update(obj)
        return obj


class CliVersion(BaseValidationVersion):
    """A model that represents the polyaxon cli version."""

    class Meta:
        app_label = 'db'

    def __str__(self):
        return 'Cli version'

    @classmethod
    def get_min_version(cls):
        import conf

        return conf.get('CLI_MIN_VERSION')

    @classmethod
    def get_latest_version(cls):
        import conf

        return conf.get('CLI_LATEST_VERSION')


class PlatformVersion(BaseValidationVersion):
    """A model that represents the polyaxon platform version."""

    class Meta:
        app_label = 'db'

    def __str__(self):
        return 'Platform version'

    @classmethod
    def get_min_version(cls):
        import conf

        return conf.get('PLATFORM_MIN_VERSION')

    @classmethod
    def get_latest_version(cls):
        import conf

        return conf.get('PLATFORM_LATEST_VERSION')


class LibVersion(BaseValidationVersion):
    """A model that represents the polyaxon lib version."""

    class Meta:
        app_label = 'db'

    def __str__(self):
        return 'Lib version'

    @classmethod
    def get_min_version(cls):
        import conf

        return conf.get('LIB_MIN_VERSION')

    @classmethod
    def get_latest_version(cls):
        import conf

        return conf.get('LIB_LATEST_VERSION')


class ChartVersion(Singleton):
    """A model that represents the polyaxon chart version."""
    version = models.CharField(max_length=16)

    class Meta:
        app_label = 'db'

    def __str__(self):
        return 'Chart version'

    @staticmethod
    def get_version():
        import conf

        return conf.get('CHART_VERSION')

    @classmethod
    def may_be_update(cls, obj):
        version = cls.get_version()

        if obj.version != version:
            obj.version = version
            obj.save()
        obj.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            try:
                obj = cls.objects.get(pk=1)
            except cls.DoesNotExist:
                obj = cls.objects.create(pk=1, version=cls.get_version())
        else:
            obj = cache.get(cls.__name__)

        cls.may_be_update(obj)
        return obj
