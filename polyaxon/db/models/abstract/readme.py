from django.db import models


class ReadmeModel(models.Model):
    readme = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def has_readme(self) -> bool:
        return bool(self.readme)
