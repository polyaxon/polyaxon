# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _


class DescribableModel(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=128)
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
        null=True)

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
