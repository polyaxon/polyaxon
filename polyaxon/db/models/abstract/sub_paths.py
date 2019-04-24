from django.db import models
from django.utils.functional import cached_property


class SubPathModel(models.Model):
    class Meta:
        abstract = True

    @cached_property
    def subpath(self) -> str:
        raise NotImplementedError()
