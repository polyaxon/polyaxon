from django.contrib.postgres.fields import JSONField
from django.db import models

from libs.resource_validation import validate_resource


class JobResources(models.Model):
    """A model that represents job resources."""
    cpu = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])
    memory = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])
    gpu = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])

    class Meta:
        app_label = 'db'
        verbose_name = 'job resources'
        verbose_name_plural = 'jobs resources'

    def __str__(self):
        def get_resource(resource, resource_name):
            if not resource:
                return ''
            return '{}: <{}-{}>'.format(resource_name,
                                        resource.get('requests'),
                                        resource.get('limits'))

        cpu = get_resource(self.cpu, 'CPU')
        memory = get_resource(self.memory, 'Memory')
        gpu = get_resource(self.gpu, 'GPU')
        resources = [cpu, memory, gpu]
        return ', '.join([r for r in resources if r])
