# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.core.validators import validate_slug
from django.db import models
from django.core.cache import cache

from libs.blacklist import validate_blacklist_name


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
