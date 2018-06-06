import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract_jobs import AbstractJob
from libs.spec_validation import validate_plugin_spec_config
from polyaxon_schemas.polyaxonfile.specification import PluginSpecification


class PluginJobBase(AbstractJob):
    """A base model for plugin jobs."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    config = JSONField(
        help_text='The compiled polyaxonfile for the plugin job.',
        validators=[validate_plugin_spec_config])
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')
    build_job = models.ForeignKey(
        'db.BuildJob',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')

    class Meta:
        app_label = 'db'
        abstract = True

    @cached_property
    def specification(self):
        return PluginSpecification(values=self.config)

    @cached_property
    def resources(self):
        return self.specification.resources

    @cached_property
    def node_selectors(self):
        return self.specification.node_selectors

    @cached_property
    def unique_name(self):
        return self.__str__()
