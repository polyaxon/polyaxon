from django.conf import settings
from django.db import models

from db.models.utils import DiffModel, NameableModel


class Search(DiffModel, NameableModel):
    """A saved search query."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='searches')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    query = models.TextField()
    is_default = models.BooleanField(default=False)

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'name'), )

    @property
    def unique_name(self):
        return '{}.{}'.format(self.project.username, self.name)
