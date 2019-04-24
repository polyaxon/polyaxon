from django.db import models


class DescribableModel(models.Model):
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def has_description(self) -> bool:
        return bool(self.description)
